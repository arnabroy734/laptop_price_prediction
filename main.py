from webcrawler import crawler, items
import pandas as pd
from urls_and_paths.path import RAW_DATA_FILE
import re
import pickle
from logs.logger import App_Logger
import time
from recommendation.recommendation import Recommendation
from urls_and_paths.path import ENCODER_FILE
from training.training import TrainBestModel
from validation.validation_raw_data import RawDataValidation
from validation.validation_raw_data import RawDataValidation
import pprint
import traceback
from app import app
# import streamlit as st

try:
    # Try to load prediction pipeline and recommendation system
    # pass
    
    app()
    # Recommendation()
    
except Exception as e:
    traceback.print_exc()
    print(f"App cannot be started due to {e}")
    

