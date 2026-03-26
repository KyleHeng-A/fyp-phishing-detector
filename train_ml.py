# train_ml.py
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from detector.dataset_loader import load_phishing_email_dataset


def train_models():
    print("Loading dataset...")
    data = load_phishing_email_dataset("phishing_email.csv")

    texts = [item["text"] for item in data]
    y = [1 if item["label"] == "phishing" else 0 for item in data]

    # --- THE CRITICAL FYP STEP: Train/Test Split ---
    print("Splitting dataset into 80% Training and 20% Testing...")
    X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=0.2, random_state=42)

    # Save the 20% unseen data into a 'vault' for the evaluation script
    os.makedirs("detector", exist_ok=True)
    joblib.dump((X_test, y_test), "detector/test_data_vault.pkl")
    print(f"Saved {len(X_test)} unseen emails to the test vault.")

    # --- DATA LEAKAGE PREVENTION ---
    # We strictly FIT the vectorizer ONLY on the training data.
    print("Vectorizing training text (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)

    # 1. Train Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train_vec, y_train)

    # 2. Train Random Forest
    print("Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)  # n_jobs=-1 uses all CPU cores!
    rf_model.fit(X_train_vec, y_train)

    print("Saving models...")
    joblib.dump(vectorizer, "detector/vectorizer.pkl")
    joblib.dump(lr_model, "detector/lr_model.pkl")
    joblib.dump(rf_model, "detector/rf_model.pkl")
    print("Training complete! Models and Test Data saved successfully.")


if __name__ == "__main__":
    train_models()