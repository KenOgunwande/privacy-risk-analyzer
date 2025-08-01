import re

def detect_pii(text):
    pii_found = {}

    # Detect emails
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if emails:
        pii_found["email"] = emails

    # Detect SSNs
    ssns = re.findall(r"\b\d{3}-\d{2}-\d{4}\b", text)
    if ssns:
        pii_found["ssn"] = ssns

    # Detect phone numbers
    phones = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    if phones:
        pii_found["phone"] = phones

    return pii_found

def mask_pii(text):
    # Simple masking of detected PII
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL]", text)
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]", text)
    text = re.sub(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", "[PHONE]", text)
    return text
