from deepface import DeepFace
from io import BytesIO
from PIL import Image
import numpy as np

# Helper to convert NumPy types to native Python types
def sanitize_result(obj):
    if isinstance(obj, dict):
        return {k: sanitize_result(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_result(v) for v in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def analyze_face(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)

    result = DeepFace.analyze(
        img_path=image_np,
        actions=['age', 'gender', 'race', 'emotion'],
        detector_backend='opencv',
        enforce_detection=False
    )

    cleaned_result = sanitize_result(result[0] if isinstance(result, list) else result)
    return cleaned_result
