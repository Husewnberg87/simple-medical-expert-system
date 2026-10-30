from flask import Flask, jsonify, render_template, request

from engine import diagnose
from knowledge_base import SYMPTOMS

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", symptoms=SYMPTOMS)


@app.get("/api/symptoms")
def symptoms():
    return jsonify(SYMPTOMS)


@app.post("/api/diagnose")
def api_diagnose():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("answers"), dict):
        return jsonify(error='Send JSON like {"answers": {"fever": "yes", ...}}'), 400
    return jsonify(diagnose(payload["answers"]))


if __name__ == "__main__":
    app.run(debug=True)
