from urls_and_paths.path import BEST_MODEL, ENCODER_FILE, PREDICTION_LOGS
from logs.logger import App_Logger
import pickle

class PredictionPipeline:
    """
    This will initialise the following things at app startup:
    1. The best model from .pkl file
    2. The encode from .pkl file
    3. The recommender from .pkl file
    4. If any initialisation fails the app will not start
    """
    def __init__(self):
        try:
            # Initialise the encoder
            with open(ENCODER_FILE, 'rb') as f:
                self.encoder = pickle.load(f)
                f.close()
                App_Logger().log(PREDICTION_LOGS, "prediction pipeline init: encoder loaded successfully")
            
            # Initialise the best model
            with open(BEST_MODEL, 'rb') as f:
                self.best_model = pickle.load(f)
                f.close()
                App_Logger().log(PREDICTION_LOGS, "prediction pipeline init: best model loaded successfully")

        except:
            App_Logger().log(PREDICTION_LOGS, "prediction pipeline init: Error in loading files")
            raise Exception('Files cannot be loaded')        
    

    def predict(self, X):
        
        # First encode the data and convert to numerical form
        X_encoded = self.encoder.transform(X)

        # Make prediction
        y_pred = self.best_model.predict(X_encoded)

        # TODO: save the X and prediction to some database 

        return y_pred