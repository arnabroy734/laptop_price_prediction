# File to store productlinks obtained from MainSpider
LINK_FILE = "./webcrawler/productlinks.csv"

# File to store raw data after scraping
RAW_DATA_FILE = "./data/raw.csv"

# File to save crawler logs
CRAWL_LOGS = "./logs/crawl_logs.txt"

# File to save preprocessing logs
PRE_LOGS = "./logs/preprocessing_logs.txt"

# File to save data encoder in .pkl format
ENCODER_FILE = "./models/encoder.pkl"

# File to save preprocessed data
PREPROCESSED_DATA_FILE = './data/preprocessed.csv'

# File to save product ids and links after dropping columns
PROD_ID_AND_LINK = "./data/product_ids_and_links_after_duplicates.csv"

# FIle to save model parameters and CV and test scores
TRAIN_LOGS = "./logs/train_logs.txt"

# File to save model files
MODELS = {
    'linear' : "./models/linear.pkl",
    'decision' : "./models/decision.pkl"
}


