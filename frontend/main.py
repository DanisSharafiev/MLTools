# To run it u can use streamlit run main.py if you are in the current directory, else use streamlit run frontend/main.py

import streamlit as st
import requests
import os
import json

API_HOST = os.getenv("API_SERVICE_HOST", "api_service")
API_PORT = os.getenv("API_SERVICE_PORT", "8000")
API_URL = f"http://{API_HOST}:{API_PORT}"

st.header("MLTools")
st.write("This site provides an easy interface with almost automatically trained ML model that runs on C++.")

st.text("First of all, to use it you have to choose a desirable model:")

with st.expander("Show description of models"):
    st.caption("""
    - **Linear Regression**: A model for predicting continuous values using a linear approach.
    - **Logistic Regression**: A model for binary classification.
    - **Decision Tree**: A tree-based model for classification and regression tasks.
    """)

st.subheader("Upload a dataset")
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv", "xlsx"], accept_multiple_files=False,
                                 help="Limit 200MB per file")
if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.write("You can now proceed with training.")

if st.button("Or find it in the database"):
    st.write("Database selection feature is under development.")

st.subheader("Choose a model")
model = st.selectbox("Choose a model", ["Linear Regression", "Logistic Regression", "Decision Tree"])

if model == "Linear Regression":
    st.subheader("Model Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        l1_input = st.text_input("Enter L1 coefficient value", value="0.0000")
        try:
            l1_coefficient = float(l1_input)
            if 0 <= l1_coefficient <= 100:
                st.write(f"L1 coefficient: {l1_coefficient:.4f}")
            else:
                st.error("Value must be between 0 and 100")
        except ValueError:
            st.error("Please enter a valid number")

    with col2:
        lr_input = st.text_input("Enter learning rate value", value="0.0001")
        try:
            learning_rate = float(lr_input)
            if 0 <= learning_rate <= 100:
                st.write(f"Learning rate: {learning_rate:.4f}")
            else:
                st.error("Value must be between 0 and 100")
        except ValueError:
            st.error("Please enter a valid number")

    with col3:
        l2_input = st.text_input("Enter L2 coefficient value", value="0.0000")
        try:
            l2_coefficient = float(l2_input)
            if 0 <= l2_coefficient <= 100:
                st.write(f"L2 coefficient: {l2_coefficient:.4f}")
            else:
                st.error("Value must be between 0 and 100")
        except ValueError:
            st.error("Please enter a valid number")
    st.write("Every value is bounded from 0 to 100")

    if st.button("Train Model"):
        st.write(
            f"Training Linear Regression with L1: {l1_coefficient}, Learning Rate: {learning_rate}, L2: {l2_coefficient}")
        try:
            response = requests.get(f"http://fastapi:8000/chetotam?arg_name={l2_coefficient}")
            response.raise_for_status()
            data = response.json()
            # Добавить потом проверку, если какие-то траблы, вывести сюда, если ввсе чики пуки, значит охуенчик
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")

elif model == "Logistic Regression":
    st.write("Logistic Regression selected. Add parameters if needed.")
elif model == "Decision Tree":
    st.write("Decision Tree selected. Add parameters if needed.")

st.write("For more details, contact support or check our documentation.")