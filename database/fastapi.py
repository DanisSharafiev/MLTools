from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List
from postgresql import PostgresClient
from s3 import S3Client

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app.state.db = PostgresClient()
    app.state.db.connect()
    app.state.db.create_tables()
    app.state.s3 = S3Client(
                access_key = "mockadmin",
                secret_key= "mockadmin",
                endpoint_url= "http://mock.ru:9000",
                bucket_name= "mock",
        )
    print("[INFO] Databases are ready")
    
@app.on_event("shutdown")
def shutdown_event():
    app.state.db.close()

@app.post("/files/")
def create_file(file: UploadFile = File(...)):
    query = "INSERT INTO files (name, content) VALUES (%s, %s) RETURNING name, content"
    result = app.state.db.execute_query(query, (file.name, file.content))
    if not result:
        raise HTTPException(status_code=400, detail="File not created")
    return result[0]

@app.get("/files/{file_name}")
def read_file(file_name: str):
    result = app.state.db.select_file(file_name)
    if not result:
        raise HTTPException(status_code=404, detail="File not found")
    return result[0]

@app.get("/files/")
def read_files():
    return app.state.db.select_all_files()