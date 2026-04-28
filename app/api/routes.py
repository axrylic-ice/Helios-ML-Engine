from fastapi import APIRouter
from app.services.inference_service import run_inference
from scripts.run_inference import LiveFXSystem

router = APIRouter()

@router.get("/health")
def health():
    return {"service": "ok"}

system = LiveFXSystem()

@app.get("/fx/decision")
def get_decision():
    result = system.step()
    return result