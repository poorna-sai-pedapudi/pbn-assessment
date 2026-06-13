from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import services, mechanics, working_hours, appointments, stats

app = FastAPI(title="PBN Assessment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router)
app.include_router(mechanics.router)
app.include_router(working_hours.router)
app.include_router(appointments.router)
app.include_router(stats.router)


@app.get("/")
def root():
    return {"message": "PBN Assessment Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}