from webcrawler import crawler, items
import pandas as pd
import re
import pickle
from logs.logger import App_Logger
import time
from preprocessing.preprocessor_main import Preprocessor
from urls_and_paths.path import ENCODER_FILE
from training.training import TrainBestModel
from prediction.prediction import PredictionPipeline
from validation.validation_prediction import PredictionValidation
from recommendation.recommendation import Recommender

# crawler.scrape_product_links()
# crawler.scrape_product_details()
# crawler.scrape_data()

# data = pipelines.test_pipeline()
# data.to_csv('train_2.csv')
# print(data)
Preprocessor().preprocess()

# TrainBestModel().find_best_model()

# try:
#     pred_pipe = PredictionPipeline()
#     X = {'Processor_Name': ['Core i7', 'Core i5'],
#         'Clock_Speed': [5, 4.6],
#         'SSD_Capacity': ['2 TB', '1 TB'],
#         'RAM': [32, 8],
#         'Graphic_Processor': ['DEDICATED', 'INTEGRATED'],
#         'Graphic_Memory' : [8, 0],
#         'Touchscreen': ['No', 'No'],
#         'Screen_Size': [40.64, 40],
#         'Screen_Resolution': [4096000, 2073600]
#     }

#     X = pd.DataFrame(X)
#     print(pred_pipe.predict(X))

# except:
#     print('Prediction pipeline cannot be initiated')




# X = {'Processor_Name': ['Core i7'],
#         'Clock_Speed': [5],
#         'SSD_Capacity': ['2 TB'],
#         'RAM': [32],
#         'Graphic_Processor': ['DEDICATED'],
#         'Graphic_Memory' : [8],
#         'Touchscreen': ['No'],
#         'Screen_Size': [40.64],
#         'Screen_Resolution': [4096000]
#     }

# X = pd.DataFrame(X)

# try:
#     PredictionValidation().validate_input(X)

# except Exception as e:
#     print(e)

# res = Recommender().recommend(X)
# print(res)


