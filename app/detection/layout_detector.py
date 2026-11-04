import cv2

def detect_layout(text):
    
    text = text.upper()
    
    if "SURNAME" in text and "GIVEN NAME" in text:
        return "new_format"
    elif "FULL NAME"  or "CARD HOLDER'S SIGNATURE"in text:
        return "old_format"
    else:
        return "unknown_format detected!"