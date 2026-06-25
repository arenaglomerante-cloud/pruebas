"""
Configuration management for GEX Quant Platform
"""

from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class MarketConfig:
    """Market configuration"""
    symbols: list = None
    default_dte_range: tuple = (7, 60)  # Days to expiration range
    default_spot_range_pct: float = 0.10  # 10% around spot
    
    def __post_init__(self):
        if self.symbols is None:
            self.symbols = ['NQ', 'NDX', 'QQQ', 'SPY']


@dataclass
class DataSourceConfig:
    """Data source configuration"""
    primary: str = 'yfinance'
    fallback: Optional[str] = 'alpha_vantage'
    
    # API keys
    alpha_vantage_key: str = os.getenv('ALPHA_VANTAGE_KEY', '')
    alpaca_api_key: str = os.getenv('ALPACA_API_KEY', '')
    alpaca_secret_key: str = os.getenv('ALPACA_SECRET_KEY', '')


@dataclass
class AnalysisConfig:
    """Analysis configuration"""
    gex_price_step: float = 0.0025  # 0.25% price steps
    gamma_flip_sensitivity: float = 0.05  # 5% threshold
    support_resistance_percentile: float = 75.0
    min_oi_threshold: int = 100  # Minimum open interest


@dataclass
class ApiConfig:
    """API configuration"""
    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///gex_analysis.db')


@dataclass
class AppConfig:
    """Main application configuration"""
    market: MarketConfig = None
    data_source: DataSourceConfig = None
    analysis: AnalysisConfig = None
    api: ApiConfig = None
    
    def __post_init__(self):
        if self.market is None:
            self.market = MarketConfig()
        if self.data_source is None:
            self.data_source = DataSourceConfig()
        if self.analysis is None:
            self.analysis = AnalysisConfig()
        if self.api is None:
            self.api = ApiConfig()


# Default configuration
DEFAULT_CONFIG = AppConfig()


if __name__ == "__main__":
    config = AppConfig()
    print(config)
