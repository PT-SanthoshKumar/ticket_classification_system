from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ml.category_rules import rule_based_category
from ml.preprocessing import clean_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample_tickets.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "ticket_category_model.joblib"


def build_pipeline():
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2))),
            ("classifier", ComplementNB()),
        ]
    )


def train_model(data_path=DATA_PATH, model_path=MODEL_PATH):
    df = pd.read_csv(data_path)
    x_train, x_test, y_train, y_test = train_test_split(
        df["ticket_text"],
        df["category"],
        test_size=0.25,
        random_state=42,
        stratify=df["category"],
    )

    model = build_pipeline()
    model.fit(x_train, y_train)

    model_predictions = model.predict(x_test)
    system_predictions = [
        rule_based_category(text) or model_prediction
        for text, model_prediction in zip(x_test, model_predictions)
    ]
    accuracy = accuracy_score(y_test, system_predictions)
    model_accuracy = accuracy_score(y_test, model_predictions)
    report = classification_report(y_test, system_predictions, zero_division=0)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    return {
        "model_path": str(model_path),
        "accuracy": accuracy,
        "model_accuracy": model_accuracy,
        "classification_report": report,
        "test_size": len(x_test),
        "train_size": len(x_train),
    }


if __name__ == "__main__":
    results = train_model()
    print(f"Model saved to: {results['model_path']}")
    print(f"Raw model accuracy: {results['model_accuracy']:.2f}")
    print(f"System accuracy with category rules: {results['accuracy']:.2f}")
    print(results["classification_report"])
