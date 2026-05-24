"""Main server side for the guess-the-number game."""

import os
import sys

from flask import Flask, jsonify, render_template, request, session


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from business.business_service import checkGuess, createNumber


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "presentation"),
    )
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

    def start_new_game():
        session["target_number"] = createNumber()
        session["attempts"] = 0

    @app.get("/")
    def index():
        if "target_number" not in session:
            start_new_game()
        return render_template("index.html")

    @app.post("/new-game")
    def new_game():
        start_new_game()
        return jsonify({"message": "New game started."})

    @app.post("/guess")
    def guess():
        data = request.get_json(silent=True) or {}
        guess_value = data.get("guess")
        print(f"Received guess: {guess_value}")  # Debugging statement

        try:
            guess_number = int(guess_value)
        except (TypeError, ValueError):
            return jsonify({"error": "Enter a whole number from 1 to 100."}), 400

        if guess_number < 1 or guess_number > 100:
            return jsonify({"error": "Enter a whole number from 1 to 100."}), 400

        if "target_number" not in session:
            start_new_game()

        session["attempts"] = session.get("attempts", 0) + 1
        result = checkGuess(guess_number, session["target_number"])

        return jsonify(
            {
                "result": result["result"],
                "message": result["message"],
                "attempts": session["attempts"],
                "status": "Won" if result["result"] == "correct" else "Keep guessing",
            }
        )

    return app


# Instantiate the app for Flask to find
app = create_app()

if __name__ == "__main__":
    port = "5000"
    app.run(debug=True, host="0.0.0.0", port=port)