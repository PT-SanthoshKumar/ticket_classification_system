import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.predict import classify_ticket, load_model
from ml.train_model import train_model


app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)
model = load_model()


@app.get("/")
def home():
    return app.send_static_file("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/classify")
def classify():
    payload = request.get_json(silent=True) or {}
    ticket_text = payload.get("ticket_text", "")

    try:
        result = classify_ticket(ticket_text, model=model)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/retrain")
def retrain():
    global model
    metrics = train_model()
    model = load_model()
    return jsonify(metrics)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
