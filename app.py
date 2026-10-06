import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)


def init_db():
  conn = sqlite3.connect("users.db")
  cursor = conn.cursor()
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, name TEXT, email TEXT)"
  )
  conn.commit()
  conn.close()


@app.route("/api/users", methods=["GET"])
def get_users():
  conn = sqlite3.connect("users.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users")
  users = cursor.fetchall()
  conn.close()
  return jsonify(users)


@app.route("/api/users", methods=["POST"])
def create_user():
  data = request.json
  name = data.get("name")
  email = data.get("email")

  # Уязвимость для Bandit (eval) и XSS:
  # eval(f"print('Creating user: {name}')")

  conn = sqlite3.connect("users.db")
  cursor = conn.cursor()

  # Небезопасный SQL-запрос (SQL Injection для TC-03)
  query = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
  cursor.executescript(query)
  conn.commit()
  conn.close()

  return jsonify({"status": "user created", "name": name}), 201


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
  conn = sqlite3.connect("users.db")
  cursor = conn.cursor()
  cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
  conn.commit()
  conn.close()
  return jsonify({"status": "deleted"}), 200


if __name__ == "__main__":
  init_db()
  # debug=True используется только для локальной разработки
  app.run(host="0.0.0.0", port=5000, debug=True)