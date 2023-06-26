from urls_and_paths.path import BEST_MODEL, ENCODER_FILE, PREDICTION_LOGS, RECOMMENDER
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
                # App_Logger().log(module='prediction', msg_type='success',  message="prediction pipeline init: encoder loaded successfully")
            
            # Initialise the best model
            with open(BEST_MODEL, 'rb') as f:
                self.best_model = pickle.load(f)
                f.close()
                # App_Logger().log(module='prediction', msg_type='success',  message="prediction pipeline init: best model loaded successfully")

        except:
            # App_Logger().log(module='prediction', msg_type='error',  message="prediction pipeline init: Error in loading files")
            raise Exception('Files cannot be loaded')        
    

    def predict(self, X):
        
        # First encode the data and convert to numerical form
        X_encoded = self.encoder.transform(X)

        # Make prediction
        y_pred = self.best_model.predict(X_encoded)

        # TODO: save the X and prediction to some database 

        return y_pred
    

class RecommendationPipeline:
    
    def __init__(self):
        """
        Try to de-serialise and initialise the recommender object
        """
        try:
            with open(RECOMMENDER, 'rb') as f:
                self.recommender = pickle.load(f)
                f.close()
            # App_Logger().log(module='prediction', msg_type='success',  message="recommendation pipeline init: recommendation system initiated successfully")
        except Exception as e:
            # App_Logger().log(module='prediction', msg_type='error',  message="recommendation system initiation failed")
            raise Exception('Files cannot be loaded')   
        

    def recommend(self, X):
        return self.recommender.recommend(X)
