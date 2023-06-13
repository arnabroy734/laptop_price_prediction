from webcrawler import crawler, items
import pandas as pd
import re
from preprocessing import pipelines

# crawler.scrape_product_links()
# crawler.scrape_product_details()

data = pipelines.test_pipeline()
data.to_csv('train_1.csv')