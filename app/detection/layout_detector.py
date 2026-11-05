import cv2
def detect_layout(text):

    normalized_text = "".join(text.upper().split())

    if "SURNAME" in normalized_text and "GIVENNAME" in normalized_text:
        return "new_format"

    elif "FULLNAME" in normalized_text:
        return "old_format"

    return "unknown_format"