from sklearn.pipeline import Pipeline
from .data_cleaning import *
from .transformation import *
import pandas as pd
from webcrawler.urls import TRAIN_DATA_FILE

preprocessing_pipeline = Pipeline([
    ('drop_duplicates', DropDuplicates()),
    ('drop_columns', DropColumns()),
    ('transformation', Transformation())
])

def test_pipeline():
    data = pd.read_csv(TRAIN_DATA_FILE, encoding='unicode_escape')
    data = preprocessing_pipeline.fit_transform(data)
    return data