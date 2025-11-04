from flask import Flask, jsonify, request
from datetime import datetime
from db_utils import get_connection

app = Flask(__name__)





meals = [
    {"id": 1, "meal_id": "Pasta Carbonara", "price": 120},
    {"id": 2, "meal_id": "Caesar Salad", "price": 90}
]

@app.route("/restaurant/meals", methods=["GET"])
def get_meals():
    return jsonify(meals)

@app.route("/restaurant/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    meal_id = data.get("meal_id")
    table_number = data.get("table_number")
    order_time = data.get("order_time")

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO orders (meal_id, table_number, order_time) VALUES (%s, %s, %s)"
    values = (meal_id, table_number, order_time)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Order created successfully",
        "meal_id": meal_id,
        "table_number": table_number,
        "order_time": order_time
    }), 201


@app.route("/restaurant/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    name = data.get("name")
    time = data.get("time")
    created_at = data.get("created_at")

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO bookings (name, time, created_at) VALUES (%s, %s, %s)"
    values = (name, time, created_at)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Booking created successfully",
        "name": name,
        "time": time,
        "created_at": created_at
    }), 201



@app.route("/restaurant/roomservice", methods=["POST"])
def roomservice():
    data = request.get_json()
    meal_id = data.get("meal_id")
    price = data.get("price")
    time = data.get("time")

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO roomservice (meal_id, price, time) VALUES (%s, %s, %s)"
    values = (meal_id, price, time)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Roomservice order created successfully",
        "meal_id": meal_id,
        "price": price,
        "time": time
    }), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)