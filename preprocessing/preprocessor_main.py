from urls_and_paths.path import RAW_DATA_FILE, PRE_LOGS, ENCODER_FILE, PREPROCESSED_DATA_FILE, DATA_AFTER_CLEANING
from logs.logger import App_Logger
from sklearn.pipeline import Pipeline, make_pipeline
from preprocessing.data_cleaning import *
from preprocessing.transformation import *
import pandas as pd
from urls_and_paths.path import RAW_DATA_FILE
from preprocessing.encoding import *
from preprocessing.imputation import *
import pickle

class Preprocessor:
    """
    Description: This class will do following steps:
    1. Read the raw data
    2. Clean and transform the raw data
    3. Do categorical feature encoding 
    4. Save the encoding file in .pkl format for feature transformation in future
    5. Impute null values in Clock_Speed feature
    6. Save the preprocessed data in .csv format
    """
    def __init__(self):
        try:
            self.data = pd.read_csv(RAW_DATA_FILE, encoding='unicode_escape')
            App_Logger().log(file_path=PRE_LOGS, log_message="preprocessing: raw data read successfully and Preprocessor object initialised")
        except:
            App_Logger().log(file_path=PRE_LOGS, log_message="preprocessing: Error in initialising Preprocessor object - raw data cannot be read")
            raise Exception('Preprocessor cannot be initialised - raw data file could not be found')

    
    def preprocess(self):
        try:
            self.data = DataCleaningPipeline().pipeline.fit_transform(self.data)

            self.data.to_csv(DATA_AFTER_CLEANING, index=False)
    
            encoder = EncodingPipeline().pipeline
            self.data = encoder.fit_transform(self.data)
            with open(ENCODER_FILE, 'wb') as f:
                pickle.dump(encoder, f)
                f.close()

            self.data = ImputerPipeline().pipeline.fit_transform(self.data)

            self.data.to_csv(PREPROCESSED_DATA_FILE, index=False)
            
            App_Logger().log(file_path=PRE_LOGS, log_message="preprocessing: data successfully preprocessed and saved")
        
        except Exception as e:
            App_Logger().log(PRE_LOGS, f"preprocessing: Error in preprocessing - {e}")




class DataCleaningPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ('drop_duplicates', DropDuplicates()),
            ('drop_columns', DropColumns()),
            ('transformation', Transformation())
        ])

class EncodingPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ('processor_encode', ProcessorEncoding()),
            ('SSD_Encoding', SSD_Encoding()),
            ('GPUEncoding', GPUEncoding()),
            ('TouchscreenEncoding', TouchscreenEncoding())
        ])

class ImputerPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ('CloclSpeedNanImputer', CloclSpeedNanImputer())
        ])