from pathlib import Path

import joblib

from ml.category_rules import rule_based_category
from ml.priority import infer_priority
from ml.train_model import MODEL_PATH, train_model


def load_model(model_path=MODEL_PATH):
    model_path = Path(model_path)
    if not model_path.exists():
        train_model(model_path=model_path)
    return joblib.load(model_path)


def classify_ticket(ticket_text, model=None):
    if not str(ticket_text).strip():
        raise ValueError("Ticket text cannot be empty.")

    model = model or load_model()
    model_category = str(model.predict([ticket_text])[0])
    category = rule_based_category(ticket_text) or model_category
    priority = infer_priority(ticket_text, predicted_category=category)

    probabilities = {}
    if hasattr(model.named_steps["classifier"], "predict_proba"):
        classes = model.named_steps["classifier"].classes_
        scores = model.predict_proba([ticket_text])[0]
        probabilities = {
            str(label): round(float(score), 3)
            for label, score in sorted(zip(classes, scores), key=lambda item: item[1], reverse=True)
        }

    return {
        "ticket_text": ticket_text,
        "category": category,
        "model_category": model_category,
        "priority": priority,
        "category_confidence": probabilities,
    }


if __name__ == "__main__":
    sample = "The app is down and our whole team cannot access customer records."
    print(classify_ticket(sample))
