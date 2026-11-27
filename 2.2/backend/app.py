
from flask import Flask, request, jsonify

app = Flask(__name__)

TODOS = []


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(TODOS)


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json(silent=True)

    if not data or "todo" not in data:
        return jsonify({"error": "Missing todo"}), 400

    todo = data["todo"].strip()

    if not todo:
        return jsonify({"error": "Todo cannot be empty"}), 400

    if len(todo) > 140:
        return jsonify({"error": "Todo is too long"}), 400

    TODOS.append(todo)

    return jsonify({"todo": todo}), 201


if __name__ == "__main__":
    print("Todo backend starting on port 8080", flush=True)
    app.run(host="0.0.0.0", port=8080)
