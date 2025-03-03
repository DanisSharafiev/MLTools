from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="API for ML models")

