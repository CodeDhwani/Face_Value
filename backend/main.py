# backend/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from recognition import analyze_face

app = FastAPI(
    title="Face-Value API",
    description="FastAPI backend for facial analysis using DeepFace.",
    version="1.0.0",
)

# ─────────────── Enable CORS ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now, allow all. Restrict in production.
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
        image_bytes: bytes = await file.read()
        result = analyze_face(image_bytes)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face analysis failed: {str(e)}"
        ) from e
