from webcrawler import crawler, items
import pandas as pd
import re
import pickle
from logs.logger import App_Logger
import time
from preprocessing.preprocessor_main import Preprocessor
from urls_and_paths.path import ENCODER_FILE
from training.training import TrainBestModel


# crawler.scrape_product_links()
# crawler.scrape_product_details()
# crawler.scrape_data()

# data = pipelines.test_pipeline()
# data.to_csv('train_2.csv')
# print(data)
# Preprocessor().preprocess()

TrainBestModel().find_best_model()


