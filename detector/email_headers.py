def analyze_email_headers(headers):
    features = {}

    from_address = headers.get("From", "")
    return_path = headers.get("Return-Path", "")
    received = headers.get("Received", "")

    features["from_return_path_mismatch"] = from_address and return_path and from_address not in return_path
    features["free_email_sender"] = any(domain in from_address for domain in ["gmail.com", "yahoo.com", "outlook.com"])
    features["suspicious_mail_server"] = "unknown" in received.lower()

    return features
