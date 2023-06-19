from urls_and_paths.path import DATA_AFTER_CLEANING, PROD_ID_AND_LINK, RAW_DATA_FILE, RECOMMENDER
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import pickle
from logs.logger import App_Logger


class Recommendation:
  """
  This class will find matching product based on given input
  In this we will use Nearest Neighbour to find 5 neaest neighbours with co-sine similarity
  """

  def __init__(self):
    """
        Steps to initialise:
        1. Initialise the dataset - the dataset after cleaning will be used
        2. Drop 'Clock_Speed', 'Screen_Size', 'price' columns - those columns will not be used in similarity
        3. Do One Hot Encoding for rest of the features 
        4. Initialise Nearest Neighbour object with n_neighbours=5 and distance type cosine
        5. Fit the encoded data
        6. Save the object to ./model folder
    """
    try:

        data = pd.read_csv(DATA_AFTER_CLEANING)

        # drop the clock speed and Screen Size and price
        data.drop(['Clock_Speed', 'Screen_Size', 'price'], axis=1, inplace=True)

        # Replace NAN values in Screen Resolution with 2,073,600 (1080 x 1920)
        data['Screen_Resolution'].fillna(2073600, inplace=True)

        # resolution to int
        data['Screen_Resolution'] = data['Screen_Resolution'].map(lambda x: int(x))

        # Covert all features as categorical
        for column in data.columns:
            data[column] = pd.Categorical(data[column])

        # Do one hot encoding
        self.encoder = OneHotEncoder(drop='first', sparse_output=False)
        data_ohe = self.encoder.fit_transform(data)

        # Nearest neighbours with co-sine
        self.cosine = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.cosine.fit(data_ohe)

        with open(RECOMMENDER, 'wb') as f:
           pickle.dump(self, f)
           f.close()
        
        App_Logger().log(module='recommendation', msg_type='success', message='Recommendation system initiated and saved successfully')
    except Exception as e:
        App_Logger().log(module='recommendation', msg_type='error', message=f'Recommendation system initiation failed due to  - {e}')

    

  def recommend(self, X):

    """
        Steps to recommend:
        1. Drop 'Clock_Speed', 'Screen_Size' from the data
        2. Convert all data to categorical and find one hot encoded data with predefined encoder
        3. Find indices of the recommended products
        4. Return the product description, image url and price to show on frontend
    """
    try:

        # Drop Clock Speed and Screen Size
        X = X.drop(['Clock_Speed', 'Screen_Size'], axis=1)

        # resolution to int
        X['Screen_Resolution'] = X['Screen_Resolution'].map(lambda x: int(x))

        # Covert all features as categorical
        for column in X.columns:
            X[column] = pd.Categorical(X[column])

        # Transform the X using existing encoder
        X = self.encoder.transform(X)
        rec_indices = self.cosine.kneighbors(X, n_neighbors=10, return_distance=False)

        # Loading the product ids and links
        prod_ids = pd.read_csv(PROD_ID_AND_LINK)
        raw_data = pd.read_csv(RAW_DATA_FILE, encoding='unicode_escape')


        result = []
        for idx in rec_indices[0]:
            product_id = prod_ids['product_id'].iloc[idx]
            product = {
                "product_description" : prod_ids['product_description'].iloc[idx],
                "product_image" : prod_ids['product_image'].iloc[idx],
                "product_price" : raw_data['price'][raw_data.product_id == product_id].values[0],
                "product_link" : prod_ids['product_link'].iloc[idx]
            }
            result.append(product)
        return result
    
    except Exception as e:
        return []

    

  