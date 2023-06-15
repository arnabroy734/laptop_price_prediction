from webcrawler import crawler, items
import pandas as pd
import re
import pipelines
import pickle
from logs.logger import App_Logger
import time

crawler.scrape_product_links()
crawler.scrape_product_details()

# data = pipelines.test_pipeline()
# data.to_csv('train_2.csv')
# print(data)
# with open('encoder.pkl', 'rb') as f:
#     encoder = pickle.load(f)
#     print(encoder['SSD_Encoding'].encoding)
#     f.close()


# data = pd.read_csv('./data/train.csv', encoding='unicode_escape')
# print(data['SSD_Capacity'].unique())



