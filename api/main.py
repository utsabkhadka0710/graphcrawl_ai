from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "success"}

@app.get("/health")
def health():
    return {"status": "success"}