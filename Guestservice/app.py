from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)


PASSWORD = "INSERT_YOUR_PASSWORD_HERE" # Replace with your actual MySQL root password (maybe we use a variable later on???)

# Checks wether your service is running
@app.route('/guestservice-is-running', methods=['GET'])
def is_running():
    return "API Gateway is running", 200

# DB get all guests
def get_all_guests_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=PASSWORD,
        database="hotel_kong_arthur"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM guests")
    guests = cursor.fetchall()

    cursor.close()
    conn.close()

    return guests



# DB post a guest
def post_guest_to_db(guest):
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=PASSWORD,
        database="hotel_kong_arthur"
    )
    cursor = conn.cursor()

    query = """
        INSERT INTO guests (
            first_name, last_name, bed_amount, guest_type,
            allergies, luggage, additional_requests, diet_requests
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        guest["First Name"],
        guest["Last Name"],
        guest["Bed Amount"],
        guest["Type"],
        json.dumps(guest["Allergies"]),
        json.dumps(guest["Luggage"]),
        json.dumps(guest["Additional Request"]),
        json.dumps(guest["Diet Request"])
    )

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def delete_guest_from_db(guest_id):
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=PASSWORD,
        database="hotel_kong_arthur"
    )
    cursor = conn.cursor()

    query = "DELETE FROM guests WHERE id = %s"
    cursor.execute(query, (guest_id,))
    conn.commit()
    cursor.close()
    conn.close()



@app.route('/guests', methods=['GET'])
def get_guests():
    try:
        guests = get_all_guests_from_db()
        return jsonify(guests), 200
    except Exception as e:
        return jsonify({"error": "Failed to load guests", "details": str(e)}), 500
    finally:
        print("GET /guests request processed.")



@app.route('/guests', methods=['POST'])
def add_guest():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        required_fields = [
            "First Name", "Last Name", "Allergies", "Bed Amount",
            "Type", "Luggage", "Additional Request", "Diet Request"
        ]

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields"}), 400

        post_guest_to_db(data)
        return jsonify({"message": "Guest added"}), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Malformed JSON or internal error", "details": str(e)}), 400
    finally:
        print("POST /guests request processed.")




@app.route('/guests/<int:guest_id>', methods=['DELETE'])
def delete_guest(guest_id):
    try:
        delete_guest_from_db(guest_id)
        return jsonify({"message": f"Guest with ID {guest_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete guest", "details": str(e)}), 500
    finally:
        print(f"DELETE /guests/{guest_id} request processed.")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
