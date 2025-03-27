from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config
from utils.tools import get_stock_data
from datetime import datetime
import logging
import dataiku


config = get_recipe_config()


# Set up logging
logging_level = config.get('logging_level', "INFO")

# Map string levels to logging constants
level_mapping = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

level = level_mapping.get(logging_level, logging.INFO)  # Default to INFO if not found

logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the logger with the script name
script_name = os.path.basename(__file__).split('.')[0]
logger = logging.getLogger(script_name)
logger.setLevel(level) 



ticker = config.get('ticker')
date_range_type = config.get('date_range_type', 'period')
period = config.get('period', '1mo')
start_date = config.get('start_date')
end_date = config.get('end_date')


# Format dates if available
if start_date:
    # Convert from Dataiku date format (milliseconds since epoch) to string
    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d')
    
if end_date:
    # Convert from Dataiku date format (milliseconds since epoch) to string
    end_date =  datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d')

# Configure logging
logger.info(f"Fetching stock data for {ticker}")
if date_range_type == 'period':
    logger.info(f"Using period: {period}")
else:
    logger.info(f"Date range: {start_date} to {end_date}")

try:
    # Fetch the stock data
    if date_range_type == 'custom' and start_date and end_date:
        df = get_stock_data(ticker, start_date=start_date, end_date=end_date)
    else:
        df = get_stock_data(ticker, period=period)
    
    # Get the output dataset
    output_name = get_output_names_for_role('data_output')[0]
    output_dataset = dataiku.Dataset(output_name)
    
    # Write to the output dataset
    output_dataset.write_with_schema(df)
    
    logger.info(f"Successfully wrote {len(df)} rows of stock data for {ticker} to {output_name}")
    
except Exception as e:
    logger.error(f"Error fetching stock data: {str(e)}")
    raise


