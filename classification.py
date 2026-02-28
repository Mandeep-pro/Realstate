import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Page Config for a better look
st.set_page_config(page_title="Iris Intelligence", page_icon="🌸", layout="centered")

# Custom CSS for animations and styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    /* Fade-in animation for results */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .prediction-container {
        animation: fadeIn 1.5s;
        padding: 20px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Helper function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 1. Cache the model and data
@st.cache_resource
def get_model():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, iris.target_names, iris.feature_names

model, target_names, feature_names = get_model()

# Load animation
lottie_flower = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m9ubts9y.json")

# 2. UI Layout
st.title("🌸 Iris Flower Classifier")
st.write("A sophisticated machine learning tool to identify Iris species.")

if lottie_flower:
    st_lottie(lottie_flower, height=200, key="flower_main")

st.divider()

# 3. Sidebar Inputs
st.sidebar.header("🔧 Adjust Features")
s_length = st.sidebar.slider("Sepal length", 4.0, 8.0, 5.8)
s_width = st.sidebar.slider("Sepal width", 2.0, 4.5, 3.0)
p_length = st.sidebar.slider("Petal length", 1.0, 7.0, 4.3)
p_width = st.sidebar.slider("Petal width", 0.1, 2.5, 1.3)

# 4. Prediction Logic
input_df = pd.DataFrame([[s_length, s_width, p_length, p_width]], columns=feature_names)
prediction = model.predict(input_df)
prediction_proba = model.predict_proba(input_df)
result = target_names[prediction[0]]

# 5. Animated Results Display
st.subheader("Analysis Results")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
    st.write("**Current Input Values**")
    st.dataframe(input_df, hide_index=True)
    
    st.write("**Classification**")
    st.success(f"Species: **{result.upper()}**")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Small animation that plays when predicting
    st.write("**Confidence Level**")
    conf_df = pd.DataFrame(prediction_proba, columns=target_names)
    st.bar_chart(conf_df.T)

st.divider()
st.info("💡 Move the sliders in the sidebar to update the prediction in real-time.")