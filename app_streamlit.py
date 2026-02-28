import streamlit as st
import pandas as pd
import numpy as np


## Title and description
st.title("Real Estate Price Predictor")


## Display a Simple text
st.write("Welcome to the Real Estate Price Predictor! This application allows you to predict the price of a property based on various features. You can select the features and the model type to see how it performs.")

## Display a DataFrame
st.write("Here is a sample of the dataset we are using for training the model:")


## create a line chart
st.write("Here is a line chart showing the trend of property prices over time:")
dates = pd.date_range(start='2020-01-01', periods=100, freq='M')
prices = np.random.rand(100) * 100000 + 200000  # Random prices between 200k and 300k
line_chart_data = pd.DataFrame({'Date': dates, 'Price': prices})
line_chart_data.set_index('Date', inplace=True)
st.line_chart(line_chart_data)
