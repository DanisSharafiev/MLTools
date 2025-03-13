from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List, Any
import pandas as pd
import MLTools

app = FastAPI()

class ModelHyperParams(BaseModel):
    l1_coefficient: float
    learning_rate: float
    l2_coefficient: float

@app.on_event("startup")
def startup_event():
    print("Starting up")

@app.post("/train")
async def train_model(df: dict, params: ModelHyperParams = None, model: str = None):
    df = pd.DataFrame(df)
    if model == "Linear Regression":
        model = MLTools.LinearRegressionModel()
        model.set_l1(params.l1_coefficient)
        model.set_l2(params.l2_coefficient)
        model.train(df)
        model = df[-1:]
PolynomialRegressionModel()
model.set_l1(0.01)
model.set_l2(0.01) 
model.train(X_list, y_list, degrees_list, 0.00005)
    return {"message": "Model trained successfully!"}

@app.post("/predict")
async def predict():
    return {"message": "Prediction made successfully!"}
