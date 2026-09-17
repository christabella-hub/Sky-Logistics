from flask import Flask, render_template, jsonify, request
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
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/quote", methods=["POST"])
def submit_quote():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO quote_requests 
        (full_name, company_name, phone_number, email, shipment_type, 
         country_of_origin, destination, goods_description, estimated_value, additional_notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("full_name"),
        data.get("company_name"),
        data.get("phone_number"),
        data.get("email"),
        data.get("shipment_type"),
        data.get("country_of_origin"),
        data.get("destination"),
        data.get("goods_description"),
        data.get("estimated_value"),
        data.get("additional_notes")
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Quote request submitted successfully!"}), 201


@app.route("/api/contact", methods=["POST"])
def submit_contact():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inquiries (full_name, email, subject, message)
        VALUES (%s, %s, %s, %s)
    """, (
        data.get("full_name"),
        data.get("email"),
        data.get("subject"),
        data.get("message")
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Message sent successfully!"}), 201


if __name__ == "__main__":
    app.run(debug=True)
