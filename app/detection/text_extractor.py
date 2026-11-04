import re
from rapidfuzz import fuzz


def extract_nationality(text):

    lines = text.splitlines()

    for i, line in enumerate(lines):

        words = re.findall(r"[A-Z]+", line.upper())

        for word in words:

            similarity = fuzz.ratio(word, "NATIONALITY")

            if similarity >= 75:

                # Search the next few lines for a valid nationality
                for next_line in lines[i + 1:i + 4]:

                    value = next_line.strip().upper()

                    if value in ["NEPALI", "NON-NEPALI"]:
                        return value

    return None


def extract_new_layout(text):

    data = {}

    patterns = {

        "nin": r"NIN[\s\S]{0,100}?([0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9])",

        "surname": (
            r"SURNAME\s*[\s:|]*\n"
            r"(?:[^\n]*\n)?"
            r"\s*([A-Z]+)"
        ),

        "given_name": (
            r"GIVEN\s*NAME\s*[\s:|]*\n"
            r"(?:[^\n]*\n)?"
            r"\s*([A-Z]+(?:\s+[A-Z]+)*)"
        ),

        "dob": (
            r"DATE\s*OF\s*BIRTH\s*[\s:|]*\n"
            r"(?:[^\n]*\n)?"
            r"\s*([0-9]{4}-[0-9]{2}-[0-9]{2})"
        )
    }

    for field, pattern in patterns.items():

        match = re.search(pattern, text, re.IGNORECASE)

        data[field] = match.group(1).strip() if match else None

    data["nationality"] = extract_nationality(text)

    return data
