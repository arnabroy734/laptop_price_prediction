from webcrawler.crawler import scrape_data
from preprocessing.preprocessor_main import Preprocessor
from recommendation.recommendation import Recommendation
from training.training import TrainBestModel
from validation.validation_raw_data import RawDataValidation
from logs.logger import App_Logger
import traceback

try:
    """
    Steps to retrain:
    1. Scrape new data 
    2. Validate raw data
    3. Preprocess the raw data
    4. Build the recommendation system
    5. Train models and find best
    """
    scrape_data()
    RawDataValidation().validate()
    Preprocessor().preprocess()
    Recommendation()
    training = TrainBestModel()
    training.find_best_model()
    training.calculate_feature_importances()

except Exception as e:
    traceback.print_exc()


