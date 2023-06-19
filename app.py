# This module is used for streamlit app
from urls_and_paths.path import RAW_DATA_FILE, PREPROCESSED_DATA_FILE
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import numpy as np
from PIL import Image
import textwrap

from validation.validation_prediction import PredictionValidation
from prediction.prediction import PredictionPipeline, RecommendationPipeline
import pprint

predictor  = None
recommender = None
validator = None

@st.cache_data
def get_processor_names():
    try:
        data = pd.read_csv(RAW_DATA_FILE, encoding='unicode_escape')
        processors = list(data['Processor_Name'].unique())
        return processors
    except:
        return []

@st.cache_data
def get_clock_speed_range():
    try:
        data = pd.read_csv(PREPROCESSED_DATA_FILE)
        min, max = data['Clock_Speed'].min(), data['Clock_Speed'].max()
        return (min, max)
    except:
        return (1, 10)

@st.cache_data
def get_ssd_capacities():
    try:
        data = pd.read_csv(RAW_DATA_FILE, encoding='unicode_escape')
        values = list(data['SSD_Capacity'].unique())
        values.remove(np.nan)
        return values
    except:
        return []

@st.cache_data
def get_ram_sizes():
    try:
        data =  pd.read_csv(PREPROCESSED_DATA_FILE)
        values = data['RAM'].map(lambda x: str(int(x)) + " GB").unique()
        return values
    except:
        return []
    
@st.cache_data
def get_gpu_sizes():
    try:
        data =  pd.read_csv(PREPROCESSED_DATA_FILE)
        values = list(data['Graphic_Memory'].map(lambda x: str(int(x)) + " GB").unique())
        values.remove('0 GB')
        return values
    except:
        return []

@st.cache_data
def get_screen_size_range():
    try:
        data = pd.read_csv(PREPROCESSED_DATA_FILE)
        min, max = data['Screen_Size'].min(), data['Screen_Size'].max()
        return (min, max)
    except:
        return (10,50)

@st.cache_resource
def initialise_resources():
    global predictor
    global recommender
    global validator

    predictor = PredictionPipeline()
    recommender = RecommendationPipeline()
    validator = PredictionValidation()


def app():
    
    st.set_page_config(page_title="Predict Laptop Price", page_icon=":desktop_computer:", layout="wide")

    # Hide hamburger menu 
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    
    with st.sidebar:
        selected = option_menu(
            menu_title="Laptop Price Predictor",
            options=["Prediction", "Dataset Used", "Application Logs"],
            default_index=0,
            menu_icon=["laptop"],
            icons=["boxes", "database", "bookmark"]
            # orientation='horizontal'
        )



    # CODE FOR PREDICTION PAGE

    if selected == "Prediction":
        # Initialise prediction and recommendation systems

        st.subheader("Select Configuration")
        col1, col2 = st.columns(2)
        with col1:
            # Processor Name Input
            processor_name = st.selectbox("Processor Name", options=get_processor_names())

            # Clock speed input
            min, max = get_clock_speed_range()
            clock_speed = st.number_input(f"Maximum CPU Clock speed (range is {min} GHz to {max} GHz)",min_value=min, max_value=max, value=min)

            # SSD input
            ssd = st.selectbox("SSD", options=["Yes", "No"])
            if ssd == "Yes":
                ssd_capacity = st.selectbox("SSD Capacity", options=get_ssd_capacities())
            else:
                ssd_capacity = st.selectbox("SSD Capacity", options=['NO_SSD'], disabled=True)
            
            # RAM
            ram = st.selectbox("RAM", options=get_ram_sizes())


        with col2:
            
            graphic_card = st.selectbox("GPU", options=['INTEGRATED', 'DEDICATED'])

            if graphic_card == "INTEGRATED":
                graphic_memory = st.selectbox("GPU Memeory", options=['0 GB'], disabled=True)
            else:
                graphic_memory = st.selectbox("GPU Memeory", options=get_gpu_sizes(), disabled=False)

            touchscreen = st.selectbox("Touchscreen", options=['Yes', 'No'])

            min, max = get_screen_size_range()
            screensize = st.number_input(f"Screensize in cm (range is {min} cm to {max} cm)", min_value=min, max_value=max)
            resolution = st.selectbox("Screen Resolution", options=['1920 x 1080', '1366 x 768', '2560 x 1600', '2160 x 1440',
                                                                    '2880 x 1800', '1920 x 1200', '3840 x 2160', '3024 x 1964',
                                                                    '3456 x 2234', '2560 x 1664', '2560 x 1440', '3200 x 2000',
                                                                    '3840 x 2400', '1080 x 1920', '3072 x 1920', '2560 x 1660',
                                                                    '1020 x 1920', '3000 x 2000', '2880 x 1620', '2496 x 1664',
                                                                    '2256 x 1504'])
        
        predict = st.button("Predict", type='primary')

        st.write("---")

        if predict:
            # Collect the input
            input_X = {
                "Processor_Name" : [processor_name],
                "Clock_Speed" : [clock_speed],
                "SSD_Capacity" : [ssd_capacity],
                "RAM" : [int(ram.split(" ")[0])],
                "Graphic_Processor" : [graphic_card],
                "Graphic_Memory" : [int(graphic_memory.split(" ")[0])],
                "Touchscreen" : [touchscreen],
                "Screen_Size" : [screensize],
                "Screen_Resolution" : [float(resolution.split(" ")[0])*float(resolution.split(" ")[2])]
            }

            input_X = pd.DataFrame(input_X)

            print(input_X.dtypes)
            

            # Try validating input, then prediction and recommendation
            try:
                initialise_resources()

                validator.validate_input(input_X)
                price_predicted = predictor.predict(input_X)[0]
                recommendations = recommender.recommend(input_X)

                st.subheader(f"Expected price for your configuration is - Rs. {int(price_predicted)}")
                
                pprint.pprint(recommendations)
                
                for idx, col in enumerate(st.columns(5, gap='large')):
                    with col:
                        product  = recommendations[idx]

                        text = textwrap.shorten(product['product_description'], width=70, placeholder="...")
                        st.image(product['product_image'])
                        st.write(f"**{text}**")
                        st.write(f"****Rs. {product['product_price']}****")

            
            except Exception as e:
                st.error(f"Something went wrong - {e}")
            st.write('')
            st.caption("**Top 5 recommendations for you**")
            




    elif selected == "Dataset Used":
        st.write("Show dataset")
    else:
        st.write("Show logs")





    


        
    






        
        
      