import pandas as pd
from urls_and_paths.path import RAW_DATA_FILE
from logs.logger import App_Logger

class RawDataValidation:
    """
    This file loads the raw data file and checks the followings
    Check the nan values in certain columns - if nan is found reject validation
    """
    def __init__(self):
        """
        Nan values are not allowed in follwoing columns:
        product_id, product_link, product_description, product_image, Processor_Name, RAM, Touchscreen, price
        """
        self.non_nan_columns = ['product_id', 'product_link', 'product_description', 'product_image', 
                           'Processor_Name', 'RAM', 'Touchscreen', 'price']
        

    def validate(self):
        # Load raw data
        data = pd.read_csv(RAW_DATA_FILE, encoding="unicode_escape")

        # Check null values and raise exception if found in certain columns
        for column in self.non_nan_columns:
            if data[column].isna().sum() != 0:
                App_Logger().log(module='validation', msg_type='error', message=f'raw data validation failed - data contains NAN value in column {column}')
                raise Exception(f"Column {column} has null values - it is not allowed")
        
        App_Logger().log(module='validation', msg_type='success', message=f'raw data validation successful')
