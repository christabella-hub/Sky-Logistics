from flask import Flask, render_template, jsonify
import os
import psycopg2

app = Flask(__name__, template_folder="../templates",
            static_folder="../static")


def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/shipments")
def get_shipments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM shipments;")
    rows = cur.fetchall()
    cur.close
    conn.close
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
