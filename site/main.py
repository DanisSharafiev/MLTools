from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="API for ML models")

@app.on_event("startup")
def startup_event():
    print("Starting up")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_location = f"uploads/{file.filename}"
        
        with open(file_location, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {"filename": file.filename, "saved_location": file_location}
    except Exception as e:
        return {"error": f"Failed to save file: {str(e)}"}

