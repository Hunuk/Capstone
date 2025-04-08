from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is working"}

@app.post("/upload-images/")
def upload_images():
    return {"message": "Images uploaded successfully"}