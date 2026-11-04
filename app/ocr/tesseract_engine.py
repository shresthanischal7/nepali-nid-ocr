import pytesseract as ts
from app.preprocessing.perspective import PerspectiveCorrector
import cv2

class TesseractEngine:
    
    def __init__(self, image, language = "nep+eng"):
        self.image = image
        self.language = language
        
    def give_ocr(self):
        editor = PerspectiveCorrector(self.image)
        editor.grayscale()
        editor.gaussian_blur()
        binary_img = editor.threshold()
        text = ts.image_to_string(binary_img, lang= self.language)
        return text

        

        
    