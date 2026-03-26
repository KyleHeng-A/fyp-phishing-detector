import re

def extract_features(text):
    text_lower = text.lower()

    features = {
        "urgent_keywords": bool(re.search(
            r"\b(urgent|verify|immediately|suspended|locked|security|alert|password)\b",
            text_lower
        )),

        "contains_click_here": bool(re.search(r"\bclick\s+here\b", text_lower)),

        "contains_login_request": bool(re.search(
            r"\b(login|log in|sign in|verify|account access)\b",
            text_lower
        )),

        "financial_urgency": bool(re.search(
            r"\b(wire|gift card|payment|invoice|transfer)\b.*\b(urgent|quick favor|end of day|immediately)\b",
            text_lower
        )),

        "brand_impersonation": bool(re.search(
            r"\b(ups|fedex|usps|dhl|amazon)\b",
            text_lower
        )),

        "excessive_capital_letters": sum(1 for c in text if c.isupper()) > 20,

        "many_exclamation_marks": text.count("!") > 3
    }

    return features

