"""
Options Chain Data Management
Handles fetching and processing options chain data from various sources
"""

import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import requests


class DataSourceBase(ABC):
    """Abstract base class for options data sources"""
    
    @abstractmethod
    def fetch_chain(self, symbol: str, expiration: str) -> pd.DataFrame:
        """Fetch options chain for given symbol and expiration"""
        pass


class OptionsChain:
    """
    Main class for managing options chain data
    
    Supports multiple data sources and data processing
    """
    
    def __init__(self, symbol: str, expiration_date: Optional[str] = None, data_source: str = 'yfinance'):
        """
        Initialize OptionsChain
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'QQQ', 'NQ')
            expiration_date: Expiration date (format: 'YYYY-MM-DD')
            data_source: Data source ('yfinance', 'alpha_vantage', 'alpaca')
        """
        self.symbol = symbol
        self.expiration_date = expiration_date
        self.data_source = data_source
        self.chain_data = None
        self.spot_price = None
    
    def fetch(self) -> pd.DataFrame:
        """Fetch options chain data"""
        
        if self.data_source == 'yfinance':
            return self._fetch_yfinance()
        elif self.data_source == 'alpha_vantage':
            return self._fetch_alpha_vantage()
        else:
            raise ValueError(f"Unknown data source: {self.data_source}")
    
    def _fetch_yfinance(self) -> pd.DataFrame:
        """Fetch from Yahoo Finance"""
        try:
            import yfinance as yf
            
            # Get ticker
            ticker = yf.Ticker(self.symbol)
            
            # Get spot price
            hist = ticker.history(period='1d')
            self.spot_price = hist['Close'].iloc[-1] if len(hist) > 0 else None
            
            # Get available expirations
            if self.expiration_date is None:
                expirations = ticker.options
                if len(expirations) == 0:
                    raise ValueError(f"No options available for {self.symbol}")
                self.expiration_date = expirations[0]
            
            # Fetch options chain
            options = ticker.option_chain(self.expiration_date)
            
            # Process calls
            calls = options.calls.copy()
            calls['option_type'] = 'C'
            calls['dte'] = self._calculate_dte(self.expiration_date)
            
            # Process puts
            puts = options.puts.copy()
            puts['option_type'] = 'P'
            puts['dte'] = self._calculate_dte(self.expiration_date)
            
            # Combine
            chain = pd.concat([calls, puts], ignore_index=True)
            
            # Standardize columns
            chain = chain.rename(columns={
                'lastPrice': 'last_price',
                'lastVolatility': 'iv',
                'openInterest': 'open_interest',
                'bid': 'bid',
                'ask': 'ask',
                'strike': 'strike',
                'volume': 'volume'
            })
            
            self.chain_data = chain
            return chain
            
        except ImportError:
            raise ImportError("yfinance not installed. Install with: pip install yfinance")
    
    def _fetch_alpha_vantage(self) -> pd.DataFrame:
        """Fetch from Alpha Vantage API"""
        # Placeholder for Alpha Vantage implementation
        raise NotImplementedError("Alpha Vantage data source not yet implemented")
    
    @staticmethod
    def _calculate_dte(expiration_date: str) -> int:
        """Calculate days to expiration"""
        exp_date = pd.to_datetime(expiration_date)
        today = pd.Timestamp.now()
        dte = (exp_date - today).days
        return max(dte, 0)
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and validate options chain data"""
        
        if self.chain_data is None:
            raise ValueError("No chain data available. Call fetch() first.")
        
        df = self.chain_data.copy()
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['strike', 'open_interest', 'iv', 'bid', 'ask'])
        
        # Filter out zero IV or OI
        df = df[df['iv'] > 0]
        df = df[df['open_interest'] > 0]
        
        # Filter valid bid-ask spreads
        df = df[df['bid'] <= df['ask']]
        
        # Calculate mid-price
        df['mid_price'] = (df['bid'] + df['ask']) / 2
        
        return df
    
    def get_strikes_near_spot(self, pct_range: float = 0.10) -> pd.DataFrame:
        """
        Get strikes near spot price
        
        Args:
            pct_range: Percentage range around spot (default 10%)
        
        Returns:
            DataFrame filtered to strikes near spot
        """
        if self.chain_data is None or self.spot_price is None:
            raise ValueError("Chain data or spot price not available")
        
        lower_bound = self.spot_price * (1 - pct_range)
        upper_bound = self.spot_price * (1 + pct_range)
        
        return self.chain_data[
            (self.chain_data['strike'] >= lower_bound) & 
            (self.chain_data['strike'] <= upper_bound)
        ]
    
    def get_calls_puts_spread(self) -> Dict:
        """Get call-put spread for analysis"""
        
        calls = self.chain_data[self.chain_data['option_type'] == 'C']
        puts = self.chain_data[self.chain_data['option_type'] == 'P']
        
        return {
            'calls': calls,
            'puts': puts,
            'total_call_oi': calls['open_interest'].sum(),
            'total_put_oi': puts['open_interest'].sum(),
            'put_call_ratio': puts['open_interest'].sum() / calls['open_interest'].sum() 
                            if calls['open_interest'].sum() > 0 else 0
        }
    
    def get_summary(self) -> Dict:
        """Get summary statistics for the chain"""
        
        if self.chain_data is None:
            raise ValueError("No chain data available")
        
        df = self.chain_data
        
        return {
            'symbol': self.symbol,
            'expiration': self.expiration_date,
            'spot_price': self.spot_price,
            'total_strikes': df['strike'].nunique(),
            'total_oi': df['open_interest'].sum(),
            'avg_iv': df['iv'].mean(),
            'bid_ask_spread': (df['ask'] - df['bid']).mean()
        }


# Example usage
if __name__ == "__main__":
    # Fetch options chain for QQQ (Nasdaq-100 ETF)
    chain = OptionsChain(symbol='QQQ', data_source='yfinance')
    data = chain.fetch()
    
    print("Raw data shape:", data.shape)
    print("\nFirst few rows:")
    print(data.head())
    
    # Clean data
    cleaned = chain.clean_data()
    print("\nCleaned data shape:", cleaned.shape)
    
    # Get summary
    summary = chain.get_summary()
    print("\nChain Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Get call-put spread
    cp_spread = chain.get_calls_puts_spread()
    print(f"\nPut/Call Ratio: {cp_spread['put_call_ratio']:.2f}")
