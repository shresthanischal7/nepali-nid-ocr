import cv2
from paddleocr import PaddleOCR

from app.detection.fuzzy_matcher import correct_ocr_labels
from app.detection.layout_detector import detect_layout

from app.detection.text_extractor import (
    extract_new_layout,
    extract_old_layout
)

class PaddleEngine:
    
    ocr = None
    
    @classmethod
    def initialize_model(cls):
        
        if cls.ocr is None:
            print('Loading PaddleOcr Model ...')
            
            cls.ocr = PaddleOCR(
                text_detection_model_name="PP-OCRv5_server_det",
                text_recognition_model_name="devanagari_PP-OCRv5_mobile_rec",
                device="cpu",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                enable_mkldnn=False
            )

    def __init__(self, image):
        self.image = image
        self.formatted_text = None
        self.layout_type = None

    def load_text(self):

        results = self.ocr.predict(self.image)

        extracted_text = []

        for result in results:

            data = result.json
            texts = data["res"]["rec_texts"]

            extracted_text.extend(texts)

        text = "\n".join(extracted_text)

        self.formatted_text = correct_ocr_labels(text)

        return self.formatted_text

    def result(self):

        text = self.load_text()

        self.layout_type = detect_layout(text)

        print("\nDetected layout:", self.layout_type)

        if self.layout_type == "old_format":

            result = extract_old_layout(text)

        elif self.layout_type == "new_format":

            result = extract_new_layout(text)

        else:

            print("Unknown NID layout detected.")
            return None

        return result
    
 