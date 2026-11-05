import re
from rapidfuzz import fuzz

def extract_nid(text):

    pattern = r"(?<![0-9])[0-9]{3}-[0-9]{3}-(?:[0-9]{3}-[0-9]|[0-9]{4})(?![0-9])"

    match = re.search(pattern, text)

    return match.group(0) if match else None


def extract_nationality(text):

    lines = text.splitlines()

    for i, line in enumerate(lines):

        words = re.findall(r"[A-Z]+", line.upper())

        for word in words:

            similarity = fuzz.ratio(word, "NATIONALITY")

            if similarity >= 75:

                for next_line in lines[i + 1:i + 5]:

                    value = next_line.strip().upper()

                    if value in ["NEPALI", "NON-NEPALI"]:
                        return value.title()

    return None

def extract_old_layout(text):

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    data = {
        "nid": None,
        "full_name": None,
        "dob": None,
        "nationality": None
    }

    # Extract NID
    data['nid'] = extract_nid(text)
    # Extract FULL NAME
    for i, line in enumerate(lines):

        if fuzz.ratio(line.upper(), "FULL NAME") >= 75:

            for next_line in lines[i + 1:i + 6]:

                upper_line = next_line.upper()

                if any(label in upper_line for label in [
                    "DATE OF ISSUE",
                    "DATE OF BIRTH",
                    "NATIONALITY",
                    "SIGNATURE",
                    "SEX"
                ]):
                    continue

                if re.fullmatch(r"[A-Z][A-Z .'-]+", upper_line):
                    data["full_name"] = next_line
                    break

            break

    # Extract DOB
    for i, line in enumerate(lines):

        if fuzz.ratio(line.upper(), "DATE OF BIRTH") >= 75:

            for next_line in lines[i + 1:i + 6]:

                match = re.search(
                    r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b",
                    next_line
                )

                if match:
                    data["dob"] = match.group(0)
                    break

            break

    # Extract nationality
    data["nationality"] = extract_nationality(text)
    return data


def extract_new_layout(text):

    patterns = {
        "surname": (
            r"SURNAME\s*[:|]?\s*\n\s*"
            r"(?:[^\n]*\n)?\s*([A-Z]+)"
        ),

        "given_name": (
            r"GIVEN\s*NAME\s*[:|]?\s*\n\s*"
            r"(?:[^\n]*\n)?\s*([A-Z]+(?:\s+[A-Z]+)*)"
        ),

        "dob": (
            r"DATE\s*OF\s*BIRTH[\s\S]{0,100}?"
            r"([0-9]{4}-[0-9]{2}-[0-9]{2})"
        )
    }

    data = {}

    for field, pattern in patterns.items():

        match = re.search(pattern, text, re.IGNORECASE)

        data[field] = match.group(1).strip() if match else None

    full_name_parts = [
        data["given_name"],
        data["surname"]
    ]

    full_name = " ".join(
        part for part in full_name_parts if part
    ) or None

    return {
        "nid": extract_nid(text),
        "full_name": full_name,
        "dob": data["dob"],
        "nationality": extract_nationality(text)
    }