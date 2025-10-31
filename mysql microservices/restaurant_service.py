from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

meals = [
    {"id": 1, "meal_id": "Pasta Carbonara", "price": 120},
    {"id": 2, "meal_id": "Caesar Salad", "price": 90}
]
orders = []
bookings = []


@app.route("/restaurant/meals", methods=["GET"])
def get_meals():
    return jsonify(meals)


@app.route("/restaurant/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    order = {
        "id": len(orders) + 1,
        "meal_id": data.get("meal_id"),
        "price": data.get("price")
    }
    orders.append(order)
    return jsonify(order), 201


@app.route("/restaurant/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    booking = {
        "id": len(bookings) + 1,
        "name": data.get("name"),
        "time": data.get("time")
    }
    bookings.append(booking)
    return jsonify(booking), 201



