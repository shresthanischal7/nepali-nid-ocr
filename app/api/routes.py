from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np
import cv2

from app.preprocessing.perspective import PerspectiveCorrector
from app.ocr.paddle_engine import PaddleEngine

router = APIRouter()

@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):

    image_bytes = await file.read()

    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported image."
        )

    corrector = PerspectiveCorrector(image)
    image = corrector.correct_perspective()

    engine = PaddleEngine(image)
    result = engine.result()

    if result is None:
        raise HTTPException(
            status_code=422,
            detail="Unable to extract information from the image. Give more clear picture."
        )

    return result