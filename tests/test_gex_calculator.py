"""Unit tests for src.core.gex_calculator.GEXCalculator"""

import numpy as np
import pandas as pd
import pytest

from src.core.gex_calculator import GEXCalculator


@pytest.fixture
def options_data():
    return pd.DataFrame(
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


class TestBlackScholesGreeks:
    def test_gamma_is_positive(self):
        result = GEXCalculator.gamma(S=100, K=100, T=0.25, r=0.05, sigma=0.2)
        assert result > 0

    def test_gamma_zero_when_expired(self):
        assert GEXCalculator.gamma(S=100, K=100, T=0, r=0.05, sigma=0.2) == 0

    def test_vega_is_positive(self):
        result = GEXCalculator.vega(S=100, K=100, T=0.25, r=0.05, sigma=0.2)
        assert result > 0

    def test_vega_zero_when_expired(self):
        assert GEXCalculator.vega(S=100, K=100, T=0, r=0.05, sigma=0.2) == 0


class TestComputeGex:
    def test_returns_dataframe_with_expected_columns(self, options_data):
        calculator = GEXCalculator(spot_price=6600)
        gex_df = calculator.compute_gex(options_data)

        assert list(gex_df.columns) == ["price", "gex"]
        assert not gex_df.empty

    def test_default_price_levels_span_5_percent_band(self, options_data):
        calculator = GEXCalculator(spot_price=6600)
        gex_df = calculator.compute_gex(options_data)

        assert gex_df["price"].min() >= 6600 * 0.95
        assert gex_df["price"].max() < 6600 * 1.05

    def test_custom_price_levels_are_respected(self, options_data):
        calculator = GEXCalculator(spot_price=6600)
        price_levels = np.array([6500.0, 6600.0, 6700.0])
        gex_df = calculator.compute_gex(options_data, price_levels=price_levels)

        assert list(gex_df["price"]) == list(price_levels)

    def test_missing_required_columns_raises(self):
        calculator = GEXCalculator(spot_price=6600)
        bad_df = pd.DataFrame({"strike": [6600]})

        with pytest.raises(ValueError):
            calculator.compute_gex(bad_df)

    def test_empty_options_df_returns_zero_gex(self):
        calculator = GEXCalculator(spot_price=6600)
        empty_df = pd.DataFrame(
            columns=["strike", "iv", "open_interest", "option_type", "dte"]
        )
        price_levels = np.array([6500.0, 6600.0])

        gex_df = calculator.compute_gex(empty_df, price_levels=price_levels)

        assert (gex_df["gex"] == 0).all()

    def test_rows_with_zero_iv_or_dte_are_skipped(self, options_data):
        calculator = GEXCalculator(spot_price=6600)
        price_levels = np.array([6600.0])

        baseline = calculator.compute_gex(options_data, price_levels=price_levels)

        with_invalid_row = pd.concat(
            [
                options_data,
                pd.DataFrame(
                    {
                        "strike": [6600],
                        "iv": [0],
                        "open_interest": [5000],
                        "option_type": ["C"],
                        "dte": [14],
                    }
                ),
            ],
            ignore_index=True,
        )

        result = calculator.compute_gex(with_invalid_row, price_levels=price_levels)

        assert np.isclose(result["gex"].iloc[0], baseline["gex"].iloc[0])

    def test_matches_reference_loop_implementation(self, options_data):
        """The vectorized implementation must match a naive per-row loop."""
        calculator = GEXCalculator(spot_price=6600)
        price_levels = np.array([6500.0, 6600.0, 6700.0])

        expected = []
        for price in price_levels:
            gex_value = 0.0
            for _, row in options_data.iterrows():
                T = row["dte"] / 365.0
                sigma = row["iv"] / 100.0
                gamma = GEXCalculator.gamma(
                    S=price, K=row["strike"], T=T, r=calculator.rate, sigma=sigma
                )
                if row["option_type"].upper() == "C":
                    gex_value += gamma * row["open_interest"] * 100
                else:
                    gex_value -= gamma * row["open_interest"] * 100
            expected.append(gex_value)

        result = calculator.compute_gex(options_data, price_levels=price_levels)

        np.testing.assert_allclose(result["gex"].to_numpy(), expected)


class TestFlipPointsAndLevels:
    def test_find_gamma_flip_points_detects_sign_change(self):
        gex_df = pd.DataFrame(
            {
                "price": [100, 101, 102, 103],
                "gex": [-5, -1, 2, 6],
            }
        )
        calculator = GEXCalculator(spot_price=101)
        flips = calculator.find_gamma_flip_points(gex_df)

        assert len(flips) >= 1
        assert flips[0]["polarity"] in {"positive", "negative"}

    def test_find_support_resistance_returns_sorted_levels(self):
        gex_df = pd.DataFrame(
            {
                "price": [95, 96, 97, 98, 99, 100],
                "gex": [-10, -8, -6, 4, 6, 8],
            }
        )
        calculator = GEXCalculator(spot_price=97)
        levels = calculator.find_support_resistance(gex_df)

        assert levels["support"] == sorted(levels["support"])
        assert levels["resistance"] == sorted(levels["resistance"])
