from urls_and_paths.path import PREPROCESSED_DATA_FILE
import pandas as pd
from logs.logger import App_Logger
from .model_linear import LinearReg
from .decision_tree import Decision

class TrainBestModel:
    """
    Description: This class will be used to 
    1. Train different models 
    2. Compare the scores the models 
    3. Save the best model with highest test score
    """
    def __init__(self):
        self.data = pd.read_csv(PREPROCESSED_DATA_FILE)
        self.models = {
            'linear' : LinearReg(),
            'decision' : Decision()
        }
        
    def find_best_model(self):
        # Tune linear regression
        # self.models['linear'].tune_parameter(self.data)
        self.models['decision'].tune_parameter(self.data)