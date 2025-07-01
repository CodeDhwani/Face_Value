# backend/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from deepface import DeepFace
import numpy as np
import cv2
import tempfile

app = FastAPI(
    title="Face-Value API",
    description="FastAPI backend for facial analysis using DeepFace with OpenCV backend only.",
    version="1.0.0",
)

# ─────────────── Enable CORS ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────── Health Check Route ───────────────
@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    return {"status": "ok", "message": "Face-Value backend running 🚀"}

# ─────────────── Analyze Face Route ───────────────
@app.post("/analyze", tags=["Face Analysis"])
async def analyze(file: UploadFile = File(...)) -> JSONResponse:
    try:
        image_bytes = await file.read()

        # Convert bytes to numpy array and then to OpenCV image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image uploaded")

        # Analyze face using only OpenCV backend
        result = DeepFace.analyze(
            img_path=img,
            actions=["age", "gender", "race", "emotion"],
            enforce_detection=True,
            detector_backend="opencv"
        )

        return JSONResponse(content=result[0])

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face analysis failed: {str(e)}"
        ) from e
