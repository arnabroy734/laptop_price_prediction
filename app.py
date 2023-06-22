# This module is used for streamlit app
from urls_and_paths.path import RAW_DATA_FILE, PREPROCESSED_DATA_FILE, DATA_AFTER_CLEANING, RAW_DATA_PROFILE, FEATURE_IMPORTANCE
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
from logs.logger import App_Logger
import streamlit_pandas as sp
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling
import plotly.express as px
import streamlit.components.v1 as components
import time


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
        # min, max = data['Screen_Size'].min(), data['Screen_Size'].max()
        # return (min, max)
        return list(data['Screen_Size'].unique())
    except:
        return []

@st.cache_resource
def initialise_resources():
    predictor = PredictionPipeline()
    recommender = RecommendationPipeline()
    validator = PredictionValidation()
    return (predictor, recommender, validator)

@st.cache_resource
def get_logs(module=None, msg_type=None):
    app_logs = App_Logger().get_logs(module, msg_type)
    app_logs = pd.DataFrame(app_logs[::-1])
    app_logs.drop(['_id'], axis=1, inplace=True)
    return app_logs

@st.cache_resource
def get_raw_data_profiling():
    with open(RAW_DATA_PROFILE, 'rb') as f:
        profile = pickle.load(f)
        f.close()
    return profile

@st.cache_resource
def get_data_after_cleaning():
    data_after_clean = pd.read_csv(DATA_AFTER_CLEANING)
    return data_after_clean

@st.cache_data
def get_feature_importances():
    feature_importances = pd.read_csv(FEATURE_IMPORTANCE)
    return feature_importances




    
st.set_page_config(page_title="Predict Laptop Price", page_icon=":desktop_computer:", layout="wide")

# Caching data and resource
predictor, recommender, validator = initialise_resources()
# raw_data_profile = get_raw_data_profiling()
app_logs = get_logs()
data_cleaned = get_data_after_cleaning()
feature_impotances = get_feature_importances()

processor_names = get_processor_names()
min_clock, max_clock = get_clock_speed_range()
ssd_capacities = get_ssd_capacities()
ram_sizes = get_ram_sizes()
gpu_sizes = get_gpu_sizes()
screen_sizes = get_screen_size_range()


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
        processor_name = st.selectbox("Processor Name", options=processor_names)

        # Clock speed input
        min, max = get_clock_speed_range()
        clock_speed = st.number_input(f"Maximum CPU Clock speed (range is {min} GHz to {max} GHz)",min_value=min_clock, max_value=max_clock, value=min_clock)

        # SSD input
        ssd = st.selectbox("SSD", options=["Yes", "No"])
        if ssd == "Yes":
            ssd_capacity = st.selectbox("SSD Capacity", options=ssd_capacities)
        else:
            ssd_capacity = st.selectbox("SSD Capacity", options=['NO_SSD'], disabled=True)
            
        # RAM
        ram = st.selectbox("RAM", options=ram_sizes)


    with col2:
            
        graphic_card = st.selectbox("GPU", options=['INTEGRATED', 'DEDICATED'])

        if graphic_card == "INTEGRATED":
            graphic_memory = st.selectbox("GPU Memeory", options=['0 GB'], disabled=True)
        else:
            graphic_memory = st.selectbox("GPU Memeory", options=gpu_sizes, disabled=False)

        touchscreen = st.selectbox("Touchscreen", options=['Yes', 'No'])

        # min, max = get_screen_size_range()
        # screensize = st.number_input(f"Screensize in cm (range is {int(min)} cm to {int(max)} cm)", min_value=min, max_value=max)
        screensize = st.selectbox(f"Screensize in cm ", options=screen_sizes)
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
        print("Prediction start")
        t1 = time.time()

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

            

        # Try validating input, then prediction and recommendation
        try:

            validator.validate_input(input_X)
            price_predicted = predictor.predict(input_X)[0]
            recommendations = recommender.recommend(input_X)

            t2 = time.time()
            print(f"Time to validate recomend and predict {t2-t1}")

            st.subheader(f"Expected price for your configuration is - Rs. {int(price_predicted)}")
                
            st.write('')
            st.caption("**Top 5 available products with similar specs for you**")

            for idx, col in enumerate(st.columns(5, gap='large')):
                with col:
                    product  = recommendations[idx]

                    text = textwrap.shorten(product['product_description'], width=70, placeholder="...")
                        
                    # st.markdown(f"[{Image(product['product_image'])}]({product['product_link']})")
                    st.image(product['product_image'])
                    st.markdown(f"[**{text}**]({product['product_link']})")
                    st.write(f"****Rs. {product['product_price']}****")
                        
        except Exception as e:
            st.error(f"Something went wrong - {e}")
            




elif selected == "Dataset Used":
    # Show Raw Data Profiling
    # st_profile_report(raw_data_profile)
    profile = open(RAW_DATA_PROFILE, 'r')
    profile = profile.read() 
    components.html(profile)

    st.subheader("Relationship of target variable with features")

    feature = st.selectbox("Choose a feature to see relationship with Price columns", options=[col for col in data_cleaned.columns if col!='price'])

    if feature in ['Clock_Speed', 'Screen_Size']:
       plot = px.scatter(data_frame=data_cleaned, x=feature, y='price', 
                         width=1200, height=600, title=f"{feature} vs Price")
       st.plotly_chart(plot) 

    else:
        plot_data = data_cleaned.groupby(feature)['price'].median()
        plot = px.bar(x=plot_data.index, y=plot_data.values, width=1200, height=600, 
                      title=f"Median Price of Laptops vs {feature}", labels={"x":f"{feature}", "y":"Median Price"})
        plot.update_xaxes(type='category')
        st.plotly_chart(plot)
    
    st.subheader("Feature importance")
    plot = px.bar(data_frame=feature_impotances, x='feature', y='importance', width=1200, height=600, 
                  title="Feature vs Feature Importance")
    st.plotly_chart(plot)
   







# CODE FOR SHOWING APPLICATION LOGS
else:
    st.subheader("Check application logs")

    def color_success_failure(val):
        if val == 'success':
            return 'color : green'
        elif val == 'error':
            return 'color : red' 
            
        
    # app_logs = app_logs.applymap(color_success_failure )
    
    # st.dataframe(app_logs,  width=1080, height=500)

        

    all_widgets = sp.create_widgets(app_logs, create_data={
        'module' : 'multiselect',
        'type' : 'multiselect',
        'message' : 'none'
    })
    res = sp.filter_df(app_logs, all_widgets)
    st.dataframe(res.style.applymap(color_success_failure), width=1080, height=500)





    


        
    






        
        
      