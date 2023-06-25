from webcrawler.crawler import scrape_data
from preprocessing.preprocessor_main import Preprocessor
from recommendation.recommendation import Recommendation
from training.training import TrainBestModel
from validation.validation_raw_data import RawDataValidation
from logs.logger import App_Logger
import traceback
from validation.validation_prediction import PredictionValidation
from prediction.prediction import PredictionPipeline, RecommendationPipeline
import pandas as pd
import time

import time 
from validation.validation_prediction import PredictionValidation
from prediction.prediction import PredictionPipeline, RecommendationPipeline
import pandas as pd

try:
    """
    Steps to retrain:
    1. Scrape new data 
    2. Validate raw data
    3. Preprocess the raw data
    4. Build the recommendation system
    5. Train models and find best
    """
    # scrape_data()
    # RawDataValidation().validate()
    # Preprocessor().preprocess()
    # Recommendation()
    # training = TrainBestModel()
    # training.find_best_model()
    # training.calculate_feature_importances()
    
    validator = PredictionValidation()
    predictor = PredictionPipeline()
    recommender = RecommendationPipeline()

    start = time.time()

    input_X = {
            "Processor_Name" : ['Core i5'],
            "Clock_Speed" : [3.5],
            "SSD_Capacity" : ['512 GB'],
            "RAM" : [16],
            "Graphic_Processor" : ['DEDICATED'],
            "Graphic_Memory" : [4],
            "Touchscreen" : ['Yes'],
            "Screen_Size" : [36.5],
            "Screen_Resolution" : [2073600.0]
        }

    input_X = pd.DataFrame(input_X)

            

        # Try validating input, then prediction and recommendation
    
    validator.validate_input(input_X)
    price_predicted = predictor.predict(input_X)[0]
    recommendations = recommender.recommend(input_X)

    end = time.time()

    print(f"Time - {end-start}")
    print(price_predicted)
    print(recommendations)

except Exception as e:
    print(e)