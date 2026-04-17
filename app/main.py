from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="FX Intelligence Engine")

app.include_router(router)