"""
GEX (Gamma Exposure) Calculator Module
Computes gamma exposure at different price levels from options chain data
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy.stats import norm


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
    
    def __init__(self, spot_price: float, rate: float = 0.05, dividend_yield: float = 0.0):
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
    def d1(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
        """Calculate d1 from Black-Scholes"""
        return (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    @staticmethod
    def d2(d1: float, sigma: float, T: float) -> float:
        """Calculate d2 from Black-Scholes"""
        return d1 - sigma * np.sqrt(T)
    
    @staticmethod
    def gamma(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
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
    def vega(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0) -> float:
        """
        Calculate vega (sensitivity to volatility change of 1%)
        Returns vega per 1% change in IV
        """
        if T <= 0:
            return 0
        
        d1_val = GEXCalculator.d1(S, K, T, r, sigma, q)
        vega = S * norm.pdf(d1_val) * np.sqrt(T) / 100
        return vega
    
    def compute_gex(self, options_df: pd.DataFrame, price_levels: Optional[np.ndarray] = None) -> pd.DataFrame:
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
        
        gex_per_level = []
        
        for price in price_levels:
            gex_value = 0
            
            for _, row in options_df.iterrows():
                try:
                    strike = row['strike']
                    iv = row['iv'] / 100  # Convert from percentage
                    oi = row['open_interest']
                    option_type = row['option_type']
                    
                    # Days to expiration
                    dte = row.get('dte', 7)  # Default to 7 days
                    T = dte / 365.0
                    
                    if T <= 0 or iv <= 0:
                        continue
                    
                    # Calculate gamma at this price level
                    gamma = self.gamma(
                        S=price,
                        K=strike,
                        T=T,
                        r=self.rate,
                        sigma=iv,
                        q=self.dividend_yield
                    )
                    
                    # GEX = sum(gamma * OI * notional per lot)
                    # For index options, typically 100 multiplier
                    notional_multiplier = 100
                    
                    # Calls contribute positive GEX from dealer perspective
                    # Puts contribute negative GEX from dealer perspective
                    if option_type.upper() == 'C':
                        gex_value += gamma * oi * notional_multiplier
                    else:  # Put
                        gex_value -= gamma * oi * notional_multiplier
                
                except Exception as e:
                    print(f"Error calculating GEX for strike {strike}: {e}")
                    continue
            
            gex_per_level.append({
                'price': price,
                'gex': gex_value
            })
        
        return pd.DataFrame(gex_per_level)
    
    def find_gamma_flip_points(self, gex_df: pd.DataFrame) -> List[Dict]:
        """
        Identify gamma flip points where GEX changes sign
        
        Args:
            gex_df: DataFrame from compute_gex()
        
        Returns:
            List of flip points with price and polarity change
        """
        gex_df = gex_df.sort_values('price').reset_index(drop=True)
        gex_df['gex_sign'] = np.sign(gex_df['gex'])
        gex_df['sign_change'] = gex_df['gex_sign'].diff() != 0
        
        flip_points = []
        for idx, row in gex_df[gex_df['sign_change']].iterrows():
            flip_points.append({
                'price': row['price'],
                'gex': row['gex'],
                'polarity': 'positive' if row['gex_sign'] > 0 else 'negative'
            })
        
        return flip_points
    
    def find_support_resistance(self, gex_df: pd.DataFrame, threshold_percentile: float = 75) -> Dict:
        """
        Identify GEX support/resistance levels
        
        Args:
            gex_df: DataFrame from compute_gex()
            threshold_percentile: Percentile threshold for identifying levels
        
        Returns:
            Dict with support and resistance levels
        """
        # Positive GEX = resistance (dealer short gamma = absorbs selling)
        positive_gex = gex_df[gex_df['gex'] > 0]
        # Negative GEX = support (dealer long gamma = absorbs buying)
        negative_gex = gex_df[gex_df['gex'] < 0]
        
        resistance_threshold = positive_gex['gex'].quantile(threshold_percentile / 100)
        support_threshold = negative_gex['gex'].quantile((100 - threshold_percentile) / 100)
        
        resistance_levels = positive_gex[positive_gex['gex'] >= resistance_threshold]['price'].tolist()
        support_levels = negative_gex[negative_gex['gex'] <= support_threshold]['price'].tolist()
        
        return {
            'resistance': sorted(resistance_levels),
            'support': sorted(support_levels)
        }


# Example usage
if __name__ == "__main__":
    # Mock options data
    options_data = pd.DataFrame({
        'strike': [6500, 6550, 6600, 6650, 6700],
        'iv': [20, 19, 18, 19, 20],
        'open_interest': [1000, 1500, 2000, 1500, 800],
        'option_type': ['C', 'C', 'C', 'P', 'P'],
        'dte': [14, 14, 14, 14, 14],
        'bid': [100, 80, 60, 30, 50],
        'ask': [102, 82, 62, 32, 52]
    })
    
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
