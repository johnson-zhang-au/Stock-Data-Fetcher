import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Union, Dict, Optional



def get_stock_data(ticker: str, 
                   start_date: Optional[str] = None, 
                   end_date: Optional[str] = None, 
                   period: str = "1mo") -> pd.DataFrame:
    """
    Retrieve historical stock data for a given ticker and time range.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL' for Apple)
        start_date (str, optional): Start date in 'YYYY-MM-DD' format
        end_date (str, optional): End date in 'YYYY-MM-DD' format
        period (str, optional): Time period if start/end dates not provided
            Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
            
    Returns:
        pd.DataFrame: DataFrame containing historical stock data
    """
    # Create ticker object
    stock = yf.Ticker(ticker)
    
    # Get historical data
    if start_date and end_date:
        hist_data = stock.history(start=start_date, end=end_date)
    else:
        hist_data = stock.history(period=period)
    
    # Reset index to make Date a column
    hist_data = hist_data.reset_index()
    
    # Ensure Date column is in string format for Dataiku compatibility
    hist_data['Date'] = hist_data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Add ticker symbol as a column for identification
    hist_data['Ticker'] = ticker
    
    return hist_data