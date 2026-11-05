from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Literal
import numpy as np
import cv2

from app.preprocessing.perspective import PerspectiveCorrector
from app.ocr.paddle_engine import PaddleEngine
from app.ocr.tesseract_engine import TesseractEngine


router = APIRouter()


@router.post("/extract")
async def extract_text(
    file: UploadFile = File(...),
    engine: Literal["paddle", "tesseract"] = "paddle"
):

    image_bytes = await file.read()

    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported image."
        )

    corrector = PerspectiveCorrector(image)

    try:
        image = corrector.correct_perspective()

    except ValueError as e:
        print(f"Perspective correction skipped: {e}")

    if engine == "paddle":
        ocr_engine = PaddleEngine(image)

    else:
        ocr_engine = TesseractEngine(image)

    result = ocr_engine.result()

    if result is None:
        raise HTTPException(
            status_code=422,
            detail="Unable to extract information from the image. Give more clear picture."
        )

    return result


@router.post("/extract-text")
async def extract_raw_text(
    file: UploadFile = File(...),
    engine: Literal["paddle", "tesseract"] = "paddle"
):

    image_bytes = await file.read()

    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported image."
        )

    corrector = PerspectiveCorrector(image)

    try:
        image = corrector.correct_perspective()

    except ValueError as e:
        print(f"Perspective correction skipped: {e}")

    if engine == "paddle":
        ocr_engine = PaddleEngine(image)

    else:
        ocr_engine = TesseractEngine(image)

    try:
        extracted_text = ocr_engine.load_text()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )

    return {
        "engine": engine,
        "extracted_text": extracted_text
    }
