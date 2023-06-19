from urls_and_paths.path import PREPROCESSED_DATA_FILE, BEST_MODEL, TRAIN_LOGS
import pandas as pd
from logs.logger import App_Logger
from .model_linear import LinearReg
from .decision_tree import Decision
from .random_forest import RandomForest
from .boosting import Boosting
import pickle

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
            'decision' : Decision(),
            'randomforest' : RandomForest(),
            'boosting' : Boosting()
        }
        
    def find_best_model(self):
        self.models['linear'].tune_parameter(self.data)
        self.models['decision'].tune_parameter(self.data)
        self.models['randomforest'].tune_parameter(self.data)
        self.models['boosting'].tune_parameter(self.data)

        # Find best model based on testscore
        sorted_models = sorted(self.models.items(), key=lambda x: x[1].test_score, reverse=True)
        best_model = sorted_models[0][1].best_model
        best_test_score = sorted_models[0][1].test_score

        # Saving the best model
        with open(BEST_MODEL, 'wb') as f:
            pickle.dump(best_model, f)
            f.close()
            App_Logger().log(module='training', msg_type='success', message=f"Training: Training is complete")
            App_Logger().log(module='training', msg_type='success', message=f"Training: Best Model: {best_model}")
            App_Logger().log(module='training', msg_type='success', message=f"Training: Best Model test score: {best_test_score}")
            App_Logger().log(module='training', msg_type='success', message=f"Training: Best Model saved: {BEST_MODEL}")
