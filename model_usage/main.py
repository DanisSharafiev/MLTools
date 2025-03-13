from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List, Any
import pandas as pd
import MLTools
import requests

app = FastAPI()

class ModelHyperParams(BaseModel):
    l1_coefficient: float
    learning_rate: float
    l2_coefficient: float

@app.on_event("startup")
def startup_event():
    app.state.model = None
    print("Starting up")

@app.post("/train")
async def train_model(df: dict, params: ModelHyperParams = None, model: str = None, polynom_degrees: List[int] = None):
    df = pd.DataFrame(df)
    if model == "Linear Regression":
        app.state.model = MLTools.LinearRegressionModel()
        app.state.model.set_l1(params.l1_coefficient)
        app.state.model.set_l2(params.l2_coefficient)
        app.state.model.train(df.drop(columns = df.columns[-1]), df[df.columns[-1]], params.learning_rate)
    elif model == "Polynomial Regression":
        app.state.model = MLTools.PolynomialRegressionModel()
        app.state.model.set_l1(params.l1_coefficient)
        app.state.model.set_l2(params.l2_coefficient)
        app.state.model.train(df.drop(columns = df.columns[-1]), df[df.columns[-1]], [polynom_degrees], params.learning_rate)
    return {"message": "Model trained successfully!"}

@app.post("/predict")
async def predict(features: List[Any]):
    if app.state.model is None:
        return {"error": "No model trained"}
    result = app.state.model.predict(features)
    return result


