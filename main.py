from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Consultório Veterinário API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Sistema de Consultório Veterinário v.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)