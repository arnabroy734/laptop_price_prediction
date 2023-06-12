from webcrawler import crawler, items
import pandas as pd
import re

# crawler.scrape_product_links()
# crawler.scrape_product_details()

df  = pd.read_csv('./data/train.csv')
print(df.head(5))