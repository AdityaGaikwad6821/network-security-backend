from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Network Security Auditor Backend is running!"}