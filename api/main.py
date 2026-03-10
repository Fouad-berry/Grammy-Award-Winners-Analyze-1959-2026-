# FastAPI pour exposer les analyses Grammy Awards
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Grammy Awards API"}

# Endpoints à compléter pour les analyses et le ML
