from fastapi import APIRouter

router = APIRouter()

system = None  # lazy init


def get_system():
    global system
    if system is None:
        from scripts.run_inference import LiveFXSystem  # lazy import
        system = LiveFXSystem()
    return system


@router.get("/health")
def health():
    return {"service": "ok"}


@router.get("/fx/decision")
def get_decision():
    sys = get_system()
    return sys.step()