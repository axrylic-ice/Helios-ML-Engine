from fastapi import APIRouter
from app.services.inference_service import run_inference

router = APIRouter()

@router.get("/health")
def health():
    return {"service": "ok"}

@router.get("/predict")
def predict():
    return run_inference()