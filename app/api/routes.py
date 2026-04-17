from fastapi import APIRouter
from app.services.inference_service import run_inference

router = APIRouter()

@router.get("/predict")
def predict():
    result = run_inference()
    return result