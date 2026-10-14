# app.py
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="static")
CORS(app)

latest_state = {"text": "", "emotion": "neutral", "speaking": False}

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/status")
def status():
    return jsonify(latest_state)

def update_state(text, emotion, speaking):
    latest_state["text"] = text
    latest_state["emotion"] = emotion
    latest_state["speaking"] = speaking

if __name__ == "__main__":
    app.run(port=5000, debug=False)