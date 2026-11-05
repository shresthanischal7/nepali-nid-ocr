from rapidfuzz import fuzz


EXPECTED_LABELS = [
    # Identity information
    "NATIONAL IDENTITY CARD",
    "NIN",
    "NATIONAL IDENTITY NUMBER",
    "Nepali"

    # Name
    "FULL NAME",
    "SURNAME",
    "GIVEN NAME",

    # Personal information
    "DATE OF BIRTH",
    "NATIONALITY",
    "SEX",

    # Dates
    "DATE OF ISSUE",
    "DATE OF DOWNLOAD",

    # Nepali labels
    "राष्ट्रिय परिचयपत्र",
    "राष्ट्रिय",
    "परिचयपत्र",
    "राष्ट्रिय परिचय नम्बर",
    "नाम थर",
    "थर",
    "नाम",
    "जन्म मिति",
    "राष्ट्रियता",
    "लिङ्ग",
    "जारी मिति",
    "डाउनलोड मिति",
    "स्थायी ठेगाना",
    "जिल्ला",
    "पालिका",
    "वडा नम्बर",
    "महिला",
    "पुरुष",
]



def correct_ocr_labels(text, threshold=80):

    lines = text.splitlines()
    corrected_lines = []

    for line in lines:

        best_match = None
        best_score = 0

        for label in EXPECTED_LABELS:

            score = fuzz.ratio(line.strip().upper(), label)

            if score > best_score:
                best_score = score
                best_match = label

        if best_score >= threshold:
            corrected_lines.append(
                line.upper().replace(line.strip().upper(), best_match)
            )
        else:
            corrected_lines.append(line)
    
    return "\n".join(corrected_lines)