from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import items
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title = "PBN Assessment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)

@app.get("/")
def root():
    return {"message": "PBN Assesssment Running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}