from fastapi import FastAPI
from .api import db, images

app = FastAPI()

app.include_router(db.router)
app.include_router(images.router)

@app.get("/")
def read_root():
    return {"message": "Healtyh Check: SmartGallery Backend is running."}













