from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from recognition import analyze_face

app = FastAPI()

# Enable CORS for frontend/backend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = analyze_face(contents)
        return JSONResponse(content=result)  # ✅ directly return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
