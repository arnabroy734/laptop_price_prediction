from urls_and_paths.path import PREPROCESSED_DATA_FILE, PROD_ID_AND_LINK, RECOMMENDATION_LOGS, ENCODER_FILE
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from logs.logger import App_Logger
import pickle

class Recommender:
    """
    This class will find matching product based on given input
    In this we will use KNN to find 5 neaest neighbours with co-sine similarity
    """
    def __init__(self):
        """
        Steps to initialise:
        1. Initialise the dataset
        2. Normalise the data to perform scaling
        3. Fit the data to KNN model with co-sine similarity
        4. Initialise the encoder from saved data
        """
        try:
            # Read preprocessed data and drop the price feature
            data = pd.read_csv(PREPROCESSED_DATA_FILE)
            data.drop(['price'], axis=1, inplace=True)

            # Scale the data before finding neighbours
            self.scaler = MinMaxScaler()
            data = self.scaler.fit_transform(data)

            # fit the data
            self.recommender = NearestNeighbors(metric='cosine', n_neighbors=5)
            self.recommender.fit(data)

            # Initialise the encoder
            with open(ENCODER_FILE, 'rb') as f:
                self.encoder = pickle.load(f)
                f.close()

            App_Logger().log(RECOMMENDATION_LOGS, "Recommender initiated successfully")

        except Exception as e:
            App_Logger().log(RECOMMENDATION_LOGS, f"Error: Recommender initiation failed - {e}")
            raise Exception("Error: Recommender initiation failed")
        

    def recommend(self, X):
        """
        Steps to recommend:
        1. Encode the data using pre-defined encoder
        2. Scale the input using predefined scaler
        3. Find indices of the recommended products
        4. Return the product links
        """
        try:
            X = self.encoder.transform(X)
            X = self.scaler.transform(X)
            rec_indices = self.recommender.kneighbors(X, n_neighbors=5, return_distance=False)
            
            # Loading the product ids and links
            prod_ids = pd.read_csv(PROD_ID_AND_LINK)

            result = []
            for idx in rec_indices[0]:
                result.append(prod_ids['product_link'].iloc[idx])
            return result
        except Exception as e:
            print(e)

