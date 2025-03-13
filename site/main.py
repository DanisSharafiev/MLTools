from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
import uvicorn
import pandas as pd
from preprocessing import preprocess_data
from typing import List, Any

app = FastAPI(title="API for ML models")

class ModelHyperParams(BaseModel):
    l1_coefficient: float
    learning_rate: float
    l2_coefficient: float
    model: str

@app.on_event("startup")
def startup_event():
    print("Starting up")
    app.state.file = None
    app.state.file_name = None
    app.state.model = None

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_location = f"uploads/{file.filename}"
        
        with open(file_location, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            app.state.file = file_location
            app.state.file_name = file.filename
        
        request = requests.post("http://fastapi:8004/", files={"file": open(file_location, "rb")})

        return {"filename": file.filename, "saved_location": file_location}
    except Exception as e:
        return {"error": f"Failed to save file: {str(e)}"}

@app.post("/train")
async def train_model(params: ModelHyperParams):
    if app.state.file is None:
        return {"error": "No file uploaded"}
    df = pd.read_csv(app.state.file)
    df = preprocess_data(df)
    app.state.model = params.model
    params = {**params, "data": df.to_dict()}
    try:
        response = requests.post("http://model:8003/train", json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to train model: {str(e)}"}
    
@app.post("/predict")
async def predict(features : List[Any]):
    df = pd.DataFrame([features])
    df = preprocess_data(df)
    try:
        response = requests.post("http://model:8003/predict", json={"features": df.to_dict()})
        response.raise_for_status()
        data = {
            "file_name": app.state.file_name,
            "features": features,
            "target": response["prediction"],
            "model_type": app.state.model
        }
        second_response = requests.post("http://database:8004/history", json={"prediction": response.json()})
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to make prediction: {str(e)}"}
    