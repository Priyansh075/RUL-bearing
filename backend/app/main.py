"""
FastAPI Application Entry Point for Bearing RUL Prediction.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router, init_model


app = FastAPI(
    title="Bearing RUL Prediction API",
    description="Predict Remaining Useful Life of rolling element bearings using XGBoost and XJTU-SY vibration features",
    version="1.0.0",
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Load model on application startup."""
    init_model()


# Register routes
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Bearing RUL Prediction API",
        "docs": "/docs",
        "version": "1.0.0",
    }
