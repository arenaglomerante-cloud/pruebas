"""Unit tests for src.core.options_chain.OptionsChain"""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.core.options_chain import OptionsChain


@pytest.fixture
def sample_chain_data():
    return pd.DataFrame(
        {
            "strike": [95, 100, 105, 95, 100, 105],
            "iv": [20, 18, 21, 19, 17, 22],
            "open_interest": [100, 200, 150, 80, 120, 60],
            "bid": [5.0, 3.0, 1.0, 1.0, 2.0, 4.0],
            "ask": [5.5, 3.5, 1.5, 1.5, 2.5, 4.5],
            "option_type": ["C", "C", "C", "P", "P", "P"],
        }
    )


class TestFetch:
    def test_unknown_data_source_raises(self):
        chain = OptionsChain(symbol="QQQ", data_source="unknown")
        with pytest.raises(ValueError):
            chain.fetch()

    def test_alpha_vantage_not_implemented(self):
        chain = OptionsChain(symbol="QQQ", data_source="alpha_vantage")
        with pytest.raises(NotImplementedError):
            chain.fetch()

    def test_fetch_yfinance_populates_chain_and_spot(self):
        mock_yf = MagicMock()
        mock_ticker = MagicMock()
        mock_yf.Ticker.return_value = mock_ticker

        mock_ticker.history.return_value = pd.DataFrame({"Close": [100.0, 101.5]})
        mock_ticker.options = ["2026-07-15"]

        calls = pd.DataFrame(
            {
                "strike": [100, 105],
                "lastPrice": [3.0, 1.5],
                "lastVolatility": [18.0, 20.0],
                "openInterest": [200, 150],
                "bid": [2.9, 1.4],
                "ask": [3.1, 1.6],
                "volume": [10, 5],
            }
        )
        puts = pd.DataFrame(
            {
                "strike": [100, 105],
                "lastPrice": [2.0, 4.0],
                "lastVolatility": [17.0, 22.0],
                "openInterest": [120, 60],
                "bid": [1.9, 3.9],
                "ask": [2.1, 4.1],
                "volume": [8, 3],
            }
        )
        mock_options_result = MagicMock()
        mock_options_result.calls = calls
        mock_options_result.puts = puts
        mock_ticker.option_chain.return_value = mock_options_result

        with patch.dict("sys.modules", {"yfinance": mock_yf}):
            chain = OptionsChain(symbol="QQQ", data_source="yfinance")
            data = chain.fetch()

        assert chain.spot_price == 101.5
        assert chain.expiration_date == "2026-07-15"
        assert set(data["option_type"]) == {"C", "P"}
        assert "open_interest" in data.columns
        assert len(data) == 4


class TestCleanData:
    def test_clean_data_requires_fetch_first(self):
        chain = OptionsChain(symbol="QQQ")
        with pytest.raises(ValueError):
            chain.clean_data()

    def test_clean_data_filters_invalid_rows(self, sample_chain_data):
        chain = OptionsChain(symbol="QQQ")
        dirty = pd.concat(
            [
                sample_chain_data,
                pd.DataFrame(
                    {
                        "strike": [110],
                        "iv": [0],
                        "open_interest": [50],
                        "bid": [1.0],
                        "ask": [1.5],
                        "option_type": ["C"],
                    }
                ),
            ],
            ignore_index=True,
        )
        chain.chain_data = dirty

        cleaned = chain.clean_data()

        assert (cleaned["iv"] > 0).all()
        assert (cleaned["open_interest"] > 0).all()
        assert (cleaned["bid"] <= cleaned["ask"]).all()
        assert "mid_price" in cleaned.columns


class TestStrikesAndSummary:
    def test_get_strikes_near_spot_filters_by_range(self, sample_chain_data):
        chain = OptionsChain(symbol="QQQ")
        chain.chain_data = sample_chain_data
        chain.spot_price = 100

        result = chain.get_strikes_near_spot(pct_range=0.05)

        assert result["strike"].min() >= 95
        assert result["strike"].max() <= 105

    def test_get_strikes_near_spot_requires_data(self):
        chain = OptionsChain(symbol="QQQ")
        with pytest.raises(ValueError):
            chain.get_strikes_near_spot()

    def test_get_calls_puts_spread(self, sample_chain_data):
        chain = OptionsChain(symbol="QQQ")
        chain.chain_data = sample_chain_data

        spread = chain.get_calls_puts_spread()

        assert spread["total_call_oi"] == 450
        assert spread["total_put_oi"] == 260
        assert spread["put_call_ratio"] == pytest.approx(260 / 450)

    def test_get_summary(self, sample_chain_data):
        chain = OptionsChain(symbol="QQQ", expiration_date="2026-07-15")
        chain.chain_data = sample_chain_data
        chain.spot_price = 100

        summary = chain.get_summary()

        assert summary["symbol"] == "QQQ"
        assert summary["expiration"] == "2026-07-15"
        assert summary["total_strikes"] == 3
        assert summary["total_oi"] == sample_chain_data["open_interest"].sum()

    def test_get_summary_requires_data(self):
        chain = OptionsChain(symbol="QQQ")
        with pytest.raises(ValueError):
            chain.get_summary()


class TestCalculateDte:
    def test_calculate_dte_never_negative(self):
        dte = OptionsChain._calculate_dte("2000-01-01")
        assert dte == 0
