# evaluate_dataset.py
import time
import joblib
import os
import concurrent.futures
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from detector.features import extract_features
from detector.rules import calculate_risk_score


def evaluate_rules_single(text):
    features = extract_features(text)
    score = calculate_risk_score(features)
    return 1 if score >= 2 else 0


def print_and_plot_metrics(y_true, y_pred, model_name):
    print(f"\n{'=' * 40}")
    print(f"Metrics for: {model_name}")
    print(f"{'=' * 40}")

    report = classification_report(y_true, y_pred, target_names=["Legitimate", "Phishing"])
    print(report)

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=["Legitimate", "Phishing"],
                yticklabels=["Legitimate", "Phishing"])

    plt.title(f"Confusion Matrix: {model_name} (Unseen Data)")
    plt.ylabel('Actual True Label')
    plt.xlabel('Model Prediction')

    filename = f"{model_name.replace(' ', '_').lower()}_matrix.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"Saved visual matrix to {filename}")


def evaluate_dataset_fast():
    print("--- Real-World Performance Evaluation ---")

    # 1. Load the UNSEEN test data instead of the whole CSV
    base_path = "detector"
    try:
        X_test, y_test = joblib.load(os.path.join(base_path, "test_data_vault.pkl"))
    except FileNotFoundError:
        print("Test data vault not found! Please run train_ml.py first.")
        return

    total = len(X_test)
    print(f"Evaluating models on {total} previously unseen emails...")

    # 2. Rule-Based Evaluation
    print("\nChecking Rules (Regex) across all CPU cores...")
    start_rules = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        rule_preds = list(executor.map(evaluate_rules_single, X_test))
    print(f"Rules evaluation took: {time.time() - start_rules:.2f} seconds")

    # 3. Machine Learning Evaluation
    print("\nLoading ML Models...")
    vectorizer = joblib.load(os.path.join(base_path, "vectorizer.pkl"))
    lr_model = joblib.load(os.path.join(base_path, "lr_model.pkl"))
    rf_model = joblib.load(os.path.join(base_path, "rf_model.pkl"))

    print("Vectorizing unseen text...")
    X_test_vec = vectorizer.transform(X_test)

    print("Running Logistic Regression batch...")
    lr_preds = lr_model.predict(X_test_vec)

    print("Running Random Forest batch...")
    rf_preds = rf_model.predict(X_test_vec)

    # 4. Generate Reports and Charts
    print_and_plot_metrics(y_test, rule_preds, "Rule-Based System")
    print_and_plot_metrics(y_test, lr_preds, "Logistic Regression")
    print_and_plot_metrics(y_test, rf_preds, "Random Forest")


if __name__ == "__main__":
    evaluate_dataset_fast()