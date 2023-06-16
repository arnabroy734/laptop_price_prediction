import pandas as pd
from urls_and_paths.path import DATA_AFTER_CLEANING, VALIDATION_LOG
from logs.logger import App_Logger

class PredictionValidation:
    """
    Checks the followings:
    1. The input should be DataFrame
    2. The input df should have predifined columns names with ordering correct
    3. Numrical columns should have values in between maximum and minimum range
    4. Categorical columns should have values from the predefined category
    """
    def __init__(self):

        try:
            # Load the preprocessed data
            data = pd.read_csv(DATA_AFTER_CLEANING)
            data.drop(['price'], axis=1, inplace=True)

            # Initiate columns names
            self.columns = list(data.columns)

            # Define types of columns:
            self.data_type = {}
            for column in self.columns:
                self.data_type[column] = data[column].dtype
        
            self.value_range = {} # Value range of numerical features - [minimum, maximum]
            self.categories = {} # Expected values of categorical features

            for column in self.columns:
                if self.data_type[column] == 'O': # Categorical
                    self.categories[column] = set(data[column].unique())
                else:
                    self.value_range[column] = [data[column].min(), data[column].max()]
            
            App_Logger().log(VALIDATION_LOG, "Prediction Validation: object initiated successfully")
        
        except:
            App_Logger().log(VALIDATION_LOG, "Prediction Validation: Error : validation object could not be initialised")
            raise Exception("validation object could not be initialised")
        

    def validate_input(self, data):
        """
        Steps: If one step is successful then go to next step
        1. validate column names and ordering 
        2. validate data type
        3. validate category for categorical data and min and max range for numerical data
        """
        try:
            self.validate_columns_names(data)
            self.validate_data_type(data)
            self.validate_category_range(data)
        except Exception as e:
            raise Exception(e)

    

    def validate_columns_names(self, data):
        """
        Check the ordering and names of the columns
        """
        for idx, input_column in enumerate(list(data.columns)):
            if self.columns[idx] != input_column:
                App_Logger().log(VALIDATION_LOG, f"Prediction Validation: input column {input_column} not matching with {self.columns[idx]}")
                raise Exception(f'Column validation failed for {input_column}')
            
        App_Logger().log(VALIDATION_LOG, f"Prediction Validation: columns names and order validated successfully")
    

    def validate_data_type(self,data):
        """
        Check whether data type is correct 
        """
        for input_column in list(data.columns):
            if self.data_type[input_column] != data[input_column].dtype:
                App_Logger().log(VALIDATION_LOG, f"Prediction Validation: data type not matching for column {input_column}")
                raise Exception(f'Data type validation failed for column {input_column}')
            
        App_Logger().log(VALIDATION_LOG, f"Prediction Validation: data type validation successful")


    def validate_category_range(self, data):
        for column in data.columns:

            if data[column].dtype == 'O':
                
                # Check for categorical data
                input_categories = set(data[column].unique())
                difference = input_categories.difference(self.categories[column])
                
                if (len(difference) != 0): # additional category found in input
                    App_Logger().log(VALIDATION_LOG, f"Prediction Validation: the category in columns {column} is not accepted")
                    raise Exception (f'New category found in column {column}')
            
            else: # Check numerical data
                min, max = self.value_range[column][0], self.value_range[column][1]
                count_beyond_range = data[column][(data[column] < min) | (data[column] > max)].count()
                if count_beyond_range != 0: # some values are beyond range
                    raise Exception(f"Value in column {column} is beyond range")
                
        
        App_Logger().log(VALIDATION_LOG, f"Prediction Validation: category and range validation successful")
                
        
