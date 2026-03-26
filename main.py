from detector.features import extract_features
from detector.url_checks import analyze_url
from detector.email_headers import analyze_email_headers

from detector.rules import calculate_risk_score, classify_hybrid


def main():
    print("=== Hybrid Phishing Detection Tool ===\n")

    message = input("Enter the message text:\n")
    url = input("\nEnter URL (leave blank if none):\n")

    features = extract_features(message)

    if url.strip():
        features.update(analyze_url(url))

    # Calculate the base rule score
    score = calculate_risk_score(features)

    # Pass BOTH the raw text and the rule score to the hybrid classifier
    classification = classify_hybrid(message, score)

    print("\n--- Analysis Result ---")
    print(f"Classification: {classification}")
    print(f"Rule Risk Score: {score}")

    print("\nDetected Rule Features:")
    for feature, detected in features.items():
        if detected:  # Only printing the triggered rules keeps the output cleaner
            print(f"- {feature}: {detected}")

    # headers = {
    #    "From": input("\nFrom address (optional): "),
    #    "Return-Path": input("Return-Path (optional): "),
    #    "Received": input("Received header (optional): ")
    # }

    # header_features = analyze_email_headers(headers)
    # features.update(header_features)

    # print("\n--- Header Analysis ---")
    # for feature, value in header_features.items():
    #    print(f"{feature}: {value}")


if __name__ == "__main__":
    main()
