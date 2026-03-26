import os
import joblib

# Load models and vectorizer
try:
    base_path = os.path.dirname(__file__)
    vectorizer = joblib.load(os.path.join(base_path, "vectorizer.pkl"))
    lr_model = joblib.load(os.path.join(base_path, "lr_model.pkl"))
    rf_model = joblib.load(os.path.join(base_path, "rf_model.pkl"))
    ML_AVAILABLE = True
except FileNotFoundError:
    ML_AVAILABLE = False
    print("Warning: ML models not found. Please run train_ml.py first.")


def calculate_risk_score(features):
    score = 0
    for detected in features.values():
        if detected:
            score += 1
    return score


def classify_message(score):
    """Original rule-based classification"""
    if score >= 4:
        return "Likely Phishing"
    elif score >= 2:
        return "Suspicious"
    else:
        return "Likely Safe"


def classify_hybrid(text, rule_score):
    """Hybrid classification using Rules, Logistic Regression, and Random Forest"""

    # 1. Rule Override for obvious cases
    if rule_score >= 4:
        return "Likely Phishing (Rule Match)"

    if not ML_AVAILABLE:
        return classify_message(rule_score)

    # 2. Get ML Predictions
    text_features = vectorizer.transform([text])
    lr_prob = lr_model.predict_proba(text_features)[0][1]
    rf_prob = rf_model.predict_proba(text_features)[0][1]

    # Average the probabilities for the final decision
    avg_prob = (lr_prob + rf_prob) / 2

    # 3. Final Decision Logic
    if avg_prob > 0.70:
        label = "Likely Phishing"
    elif avg_prob > 0.40 or rule_score >= 2:
        label = "Suspicious"
    else:
        label = "Likely Safe"

    return f"{label} (LR: {lr_prob:.1%}, RF: {rf_prob:.1%}, Rules: {rule_score})"