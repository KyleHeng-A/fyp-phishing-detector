import csv
import sys

csv.field_size_limit(sys.maxsize)


def load_phishing_email_dataset(file_path):
    dataset = []

    with open(file_path, newline="", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text = row["text_combined"]
            label = row["label"].lower()

            if label in ["phishing", "1", "spam"]:
                label = "phishing"
            else:
                label = "legitimate"

            dataset.append({
                "text": text,
                "label": label
            })

    return dataset
