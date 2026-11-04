
from app.preprocessing.image_loader import Loader
from app.preprocessing.perspective import PerspectiveCorrector


class OCRPipeline:

    def __init__(self, image_path, engine="pdl"):
        self.image_path = image_path
        self.engine = engine.lower()

    def process(self):

        # Load image
        loader = Loader(self.image_path)
        image = loader.load_image()

        # Correct perspective
        corrector = PerspectiveCorrector(image)
        image = corrector.correct_perspective()

        # Select OCR engine
        if self.engine == "pdl":

            from app.ocr.paddle_engine import PaddleEngine

            ocr = PaddleEngine(image)

        elif self.engine == "ts":

            from app.ocr.tesseract_engine import TesseractEngine

            ocr = TesseractEngine(image)

            return ocr.give_ocr()

        else:
            raise ValueError("Engine must be 'pdl' or 'ts'.")

        return ocr.result()
