"""
app.py

Flask web app — single page.
- GET  /        -> renders the page
- POST /process -> takes the submitted text, runs the CrewAI pipeline,
                    returns the result as JSON for the page to display
"""

import os
import traceback
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # reads .env file into environment variables

from crew_setup import run_pipeline  # noqa: E402 (import after load_dotenv on purpose)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please provide some text to process."}), 400

    if len(text) > 8000:
        return jsonify({"error": "Text is too long. Please keep it under 8000 characters."}), 400

    if not os.environ.get("GROQ_API_KEY"):
        return jsonify({"error": "Server is missing GROQ_API_KEY. Check your .env file."}), 500

    try:
        result = run_pipeline(text)
        return jsonify({"result": result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Something went wrong: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
