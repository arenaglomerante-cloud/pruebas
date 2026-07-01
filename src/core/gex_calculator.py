"""
GEX (Gamma Exposure) Calculator Module
Computes gamma exposure at different price levels from options chain data
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy.stats import norm

logger = logging.getLogger(__name__)


@dataclass
class BlackScholesInputs:
    """Inputs for Black-Scholes calculation"""

    spot: float
    strike: float
    maturity_years: float
    rate: float
    volatility: float
    dividend_yield: float = 0.0


class GEXCalculator:
    """
    Calculate Gamma Exposure (GEX) metrics from options chain data

    GEX represents the aggregate gamma exposure of all option positions at a given price level.
    Positive GEX = gamma long (dealers short gamma)
    Negative GEX = gamma short (dealers long gamma)
    """

    def __init__(
        self, spot_price: float, rate: float = 0.05, dividend_yield: float = 0.0
    ):
        """
        Initialize GEX Calculator

        Args:
            spot_price: Current underlying price
            rate: Risk-free rate (default 5%)
            dividend_yield: Dividend yield for the underlying
        """
        self.spot_price = spot_price
        self.rate = rate
        self.dividend_yield = dividend_yield

    @staticmethod
    def d1(
        S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0
    ) -> float:
        """Calculate d1 from Black-Scholes"""
        return (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    @staticmethod
    def d2(d1: float, sigma: float, T: float) -> float:
        """Calculate d2 from Black-Scholes"""
        return d1 - sigma * np.sqrt(T)

    @staticmethod
    def gamma(
        S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0
    ) -> float:
        """
        Calculate gamma using Black-Scholes
        Gamma = derivative of delta with respect to spot price
        """
        if T <= 0:
            return 0

        d1_val = GEXCalculator.d1(S, K, T, r, sigma, q)
        gamma = norm.pdf(d1_val) / (S * sigma * np.sqrt(T))
        return gamma

    @staticmethod
    def vega(
        S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0
    ) -> float:
        """
        Calculate vega (sensitivity to volatility change of 1%)
        Returns vega per 1% change in IV
        """
        if T <= 0:
            return 0

        d1_val = GEXCalculator.d1(S, K, T, r, sigma, q)
        vega = S * norm.pdf(d1_val) * np.sqrt(T) / 100
        return vega

    def compute_gex(
        self, options_df: pd.DataFrame, price_levels: Optional[np.ndarray] = None
    ) -> pd.DataFrame:
        """
        Calculate GEX at different price levels

        Args:
            options_df: DataFrame with columns [strike, iv, open_interest, option_type, bid, ask]
                       option_type: 'C' for call, 'P' for put
            price_levels: Array of price levels to compute GEX (default: spot ±5% by 0.25%)

        Returns:
            DataFrame with price levels and corresponding GEX values
        """

        if price_levels is None:
            # Generate price levels around spot price
            lower = self.spot_price * 0.95
            upper = self.spot_price * 1.05
            price_levels = np.arange(lower, upper, self.spot_price * 0.0025)

        price_levels = np.asarray(price_levels, dtype=float)

        required_columns = {"strike", "iv", "open_interest", "option_type"}
        missing_columns = required_columns - set(options_df.columns)
        if missing_columns:
            raise ValueError(
                f"options_df is missing required columns: {sorted(missing_columns)}"
            )

        if options_df.empty or len(price_levels) == 0:
            return pd.DataFrame(
                {"price": price_levels, "gex": np.zeros(len(price_levels))}
            )

        strikes = options_df["strike"].to_numpy(dtype=float)
        iv = options_df["iv"].to_numpy(dtype=float) / 100.0  # Convert from percentage
        oi = options_df["open_interest"].to_numpy(dtype=float)
        option_type = options_df["option_type"].astype(str).str.upper().to_numpy()

        # Days to expiration (default to 7 days when missing)
        if "dte" in options_df.columns:
            dte = options_df["dte"].fillna(7).to_numpy(dtype=float)
        else:
            dte = np.full(len(options_df), 7.0)
        maturity = dte / 365.0

        # Filter out rows with invalid maturity or volatility
        valid_mask = (maturity > 0) & (iv > 0)
        n_invalid = int((~valid_mask).sum())
        if n_invalid:
            invalid_strikes = strikes[~valid_mask]
            logger.warning(
                "Skipping %d option row(s) with non-positive maturity or IV (strikes: %s)",
                n_invalid,
                invalid_strikes.tolist(),
            )

        strikes = strikes[valid_mask]
        iv = iv[valid_mask]
        oi = oi[valid_mask]
        option_type = option_type[valid_mask]
        maturity = maturity[valid_mask]

        if len(strikes) == 0:
            return pd.DataFrame(
                {"price": price_levels, "gex": np.zeros(len(price_levels))}
            )

        # Vectorized gamma computation via broadcasting: rows = price levels, cols = options
        S = price_levels.reshape(-1, 1)
        K = strikes.reshape(1, -1)
        T = maturity.reshape(1, -1)
        sigma = iv.reshape(1, -1)

        with np.errstate(divide="ignore", invalid="ignore"):
            d1_matrix = (
                np.log(S / K) + (self.rate - self.dividend_yield + 0.5 * sigma**2) * T
            ) / (sigma * np.sqrt(T))
            gamma_matrix = norm.pdf(d1_matrix) / (S * sigma * np.sqrt(T))

        # GEX = sum(gamma * OI * notional per lot)
        # For index options, typically 100 multiplier
        notional_multiplier = 100

        # Calls contribute positive GEX from dealer perspective, puts negative
        sign = np.where(option_type == "C", 1.0, -1.0).reshape(1, -1)
        contribution = gamma_matrix * oi.reshape(1, -1) * notional_multiplier * sign
        gex_values = np.nansum(contribution, axis=1)

        return pd.DataFrame({"price": price_levels, "gex": gex_values})

    def find_gamma_flip_points(self, gex_df: pd.DataFrame) -> List[Dict]:
        """
        Identify gamma flip points where GEX changes sign

        Args:
            gex_df: DataFrame from compute_gex()

        Returns:
            List of flip points with price and polarity change
        """
        gex_df = gex_df.sort_values("price").reset_index(drop=True)
        gex_df["gex_sign"] = np.sign(gex_df["gex"])
        gex_df["sign_change"] = gex_df["gex_sign"].diff() != 0

        flip_points = []
        for idx, row in gex_df[gex_df["sign_change"]].iterrows():
            flip_points.append(
                {
                    "price": row["price"],
                    "gex": row["gex"],
                    "polarity": "positive" if row["gex_sign"] > 0 else "negative",
                }
            )

        return flip_points

    def find_support_resistance(
        self, gex_df: pd.DataFrame, threshold_percentile: float = 75
    ) -> Dict:
        """
        Identify GEX support/resistance levels

        Args:
            gex_df: DataFrame from compute_gex()
            threshold_percentile: Percentile threshold for identifying levels

        Returns:
            Dict with support and resistance levels
        """
        # Positive GEX = resistance (dealer short gamma = absorbs selling)
        positive_gex = gex_df[gex_df["gex"] > 0]
        # Negative GEX = support (dealer long gamma = absorbs buying)
        negative_gex = gex_df[gex_df["gex"] < 0]

        resistance_threshold = positive_gex["gex"].quantile(threshold_percentile / 100)
        support_threshold = negative_gex["gex"].quantile(
            (100 - threshold_percentile) / 100
        )

        resistance_levels = positive_gex[positive_gex["gex"] >= resistance_threshold][
            "price"
        ].tolist()
        support_levels = negative_gex[negative_gex["gex"] <= support_threshold][
            "price"
        ].tolist()

        return {
            "resistance": sorted(resistance_levels),
            "support": sorted(support_levels),
        }


# Example usage
if __name__ == "__main__":
    # Mock options data
    options_data = pd.DataFrame(
        {
            "strike": [6500, 6550, 6600, 6650, 6700],
            "iv": [20, 19, 18, 19, 20],
            "open_interest": [1000, 1500, 2000, 1500, 800],
            "option_type": ["C", "C", "C", "P", "P"],
            "dte": [14, 14, 14, 14, 14],
            "bid": [100, 80, 60, 30, 50],
            "ask": [102, 82, 62, 32, 52],
        }
    )

    calculator = GEXCalculator(spot_price=6600)
    gex_results = calculator.compute_gex(options_data)
    flip_points = calculator.find_gamma_flip_points(gex_results)
    levels = calculator.find_support_resistance(gex_results)

    print("GEX Results:")
    print(gex_results)
    print("\nFlip Points:")
    print(flip_points)
    print("\nSupport/Resistance:")
    print(levels)
