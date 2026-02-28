import streamlit as st

import pandas as pd

st.title("Real Estate Price Predictor") 

name = st.text_input("Enter your name:")    


age = st.slider("Select your age:", 0, 100, 25)

st.write(f"Your age is: {age}") 
if name:
    st.write(f"Hello, {name}! Welcome to the Real Estate Price Predictor!") 

option = st.selectbox("Select a model type:", ["Linear Regression", "Random Forest", "Gradient Boosting"])
st.write(f"You selected: {option}")


data = {
    "Feature 1": [1, 2, 3, 4, 5],
    "Feature 2": [10, 20, 30, 40, 50],
    "Price": [100000, 150000, 200000, 250000, 300000]
}

df = pd.DataFrame(data)
df.to_csv("sample_data.csv", index=False)




df = pd.DataFrame(data)
st.write("Here is a sample of the dataset we are using for training the model:")    

uploaded_file = st.file_uploader("Upload your dataset (CSV format):", type=["csv"])
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)
    st.write("Your uploaded dataset:")
    st.dataframe(user_data)     