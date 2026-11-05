import pytesseract as ts

from app.preprocessing.perspective import PerspectiveCorrector

from app.detection.fuzzy_matcher import correct_ocr_labels
from app.detection.layout_detector import detect_layout

from app.detection.text_extractor import (
    extract_new_layout,
    extract_old_layout
)


class TesseractEngine:

    def __init__(self, image, language="nep+eng"):
        self.image = image
        self.language = language
        self.formatted_text = None
        self.layout_type = None

    def load_text(self):

        editor = PerspectiveCorrector(self.image)

        editor.grayscale()
        editor.gaussian_blur()

        binary_img = editor.threshold()

        text = ts.image_to_string(
            binary_img,
            lang=self.language
        )

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
