from sklearn.pipeline import Pipeline, make_pipeline
from preprocessing.data_cleaning import *
from preprocessing.transformation import *
import pandas as pd
from webcrawler.urls import TRAIN_DATA_FILE
from preprocessing.encoding import *
from preprocessing.imputation import *
import pickle


class DataCleaningPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ('drop_duplicates', DropDuplicates()),
            ('drop_columns', DropColumns()),
            ('transformation', Transformation())
        ])

class EncodingPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ('processor_encode', ProcessorEncoding()),
            ('SSD_Encoding', SSD_Encoding()),
            ('GPUEncoding', GPUEncoding()),
            ('TouchscreenEncoding', TouchscreenEncoding())
        ])

class ImputerPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ('CloclSpeedNanImputer', CloclSpeedNanImputer())
        ])



def test_pipeline():
    data = pd.read_csv(TRAIN_DATA_FILE, encoding='unicode_escape')
    data = DataCleaningPipeline().pipeline.fit_transform(data)
    
    encoder = EncodingPipeline().pipeline
    data = encoder.fit_transform(data)
    with open('encoder.pkl', 'wb') as f:
        pickle.dump(encoder, f)
        f.close()

    data = ImputerPipeline().pipeline.fit_transform(data)
    return data
    