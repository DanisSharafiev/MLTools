from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List, Any

app = FastAPI()

class ModelHyperParams(BaseModel):
    l1_coefficient: float
    learning_rate: float
    l2_coefficient: float

@app.on_event("startup")
def startup_event():
    print("Starting up")

@app.post("/train")
async def train_model(file: UploadFile = File(...), params: ModelHyperParams = None):
    return {"message": "Model trained successfully!"}

@app.post("/predict")
async def predict():
    return {"message": "Prediction made successfully!"}
