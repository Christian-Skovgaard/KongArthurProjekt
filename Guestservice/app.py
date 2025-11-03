# All possible requests for Guestservice:
# GET:
# http://127.0.0.1:5000/guestservice-is-running
# http://127.0.0.1:5000/guests/all
# http://127.0.0.1:5000/guests/<id>
# http://127.0.0.1:5000/guests/by-last-name?name=
# POST:
# http://127.0.0.1:5000/guests     (in body, use 'guest.json for format)
# DELETE:
# http://127.0.0.1:5000/guests/<id>
# http://127.0.0.1:5000/guests/by-last-name?last=&first=


# SQL table format:
'''
CREATE TABLE guests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    bed_amount INT,
    guest_type VARCHAR(50),
    allergies JSON,
    luggage JSON,
    additional_requests JSON,
    diet_requests JSON
);
'''



##################################################################
# DB Connections Establisment
##################################################################



from flask import Flask, request, jsonify
import mysql.connector
import json



app = Flask(__name__)

PASSWORD = "Ridder" # Replace with your actual DB password - Default app password: PASSWORD = Ridder



# Checks wether your service is running = http://127.0.0.1:5000/guestservice-is-running
@app.route('/guestservice-is-running', methods=['GET'])
def is_running():
    return "Guestservice is running", 200



# '''
# Connection establishment to DB Online
def connection():
    return mysql.connector.connect(
        host="kingofthetable.duckdns.org",
        port=3306,
        user="app",
        password=PASSWORD,
        database="hotel_kong_arthur"
    )
'''
# Connection establishment to DB Local
def connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=PASSWORD,
        database="hotel_kong_arthur"
    )
'''



##################################################################
# DB connection functions
##################################################################



# DB get all guests
def get_all_guests_from_db():
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM guests")
    guests = cursor.fetchall()

    cursor.close()
    conn.close()

    return guests



# DB get a single guest by ID
def get_guest_by_id_from_db(guest_id):
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM guests WHERE id = %s"
    cursor.execute(query, (guest_id,))
    guest = cursor.fetchone()

    cursor.close()
    conn.close()

    return guest



# DB get guests by last name
def get_guests_by_last_name_from_db(last_name):
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM guests WHERE last_name = %s"
    cursor.execute(query, (last_name,))
    guests = cursor.fetchall()

    cursor.close()
    conn.close()

    return guests



# DB post a guest
def post_guest_to_db(guest):
    conn = connection()
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



# DB delete a guest by ID
def delete_guest_from_db(guest_id):
    conn = connection()
    cursor = conn.cursor()

    query = "DELETE FROM guests WHERE id = %s"
    cursor.execute(query, (guest_id,))
    conn.commit()
    cursor.close()
    conn.close()



# DB delete guests by first and last name
def delete_guest_by_full_name_from_db(first_name, last_name):
    conn = connection()
    cursor = conn.cursor()

    query = "DELETE FROM guests WHERE first_name = %s AND last_name = %s"
    cursor.execute(query, (first_name, last_name))
    affected_rows = cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()

    return affected_rows



##################################################################
# Request Handlers
##################################################################



# GET all guests = http://127.0.0.1:5000/guests
@app.route('/guests/all', methods=['GET'])
def get_guests():
    try:
        guests = get_all_guests_from_db()
        return jsonify(guests), 200
    except Exception as e:
        return jsonify({"error": "Failed to load guests", "details": str(e)}), 500
    finally:
        print("GET /guests request processed.")



# GET a single guest by ID = http://127.0.0.1:5000/guests/<id>
@app.route('/guests/<int:guest_id>', methods=['GET'])
def get_guest_by_id(guest_id):
    try:
        guest = get_guest_by_id_from_db(guest_id)
        if guest:
            return jsonify(guest), 200
        else:
            return jsonify({"error": "Guest not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to load guest", "details": str(e)}), 500
    finally:
        print(f"GET /guests/{guest_id} request processed.")



# GET guests by last name = http://127.0.0.1:5000/guests/by-last-name?name=
@app.route('/guests/by-last-name', methods=['GET'])
def get_guests_by_last_name():
    try:
        last_name = request.args.get('name')
        if not last_name:
            return jsonify({"error": "Missing 'name' query parameter"}), 400

        guests = get_guests_by_last_name_from_db(last_name)
        if guests:
            return jsonify(guests), 200
        else:
            return jsonify({"message": f"No guests found with last name '{last_name}'"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to load guests", "details": str(e)}), 500
    finally:
        print(f"GET /guests/by-last-name?name={last_name} request processed.")



# POST a guest = http://127.0.0.1:5000/guests     (in body, use 'guest.json for format)
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



# DELETE a guest = http://127.0.0.1:5000/guests/<id>
@app.route('/guests/<int:guest_id>', methods=['DELETE'])
def delete_guest(guest_id):
    try:
        delete_guest_from_db(guest_id)
        return jsonify({"message": f"Guest with ID {guest_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete guest", "details": str(e)}), 500
    finally:
        print(f"DELETE /guests/{guest_id} request processed.")



# DELETE guests by first and last name = http://127.0.0.1:5000/guests/by-last-name?last=&first=
@app.route('/guests/by-full-name', methods=['DELETE'])
def delete_guest_by_full_name():
    try:
        last_name = request.args.get('last')
        first_name = request.args.get('first')

        if not first_name or not last_name:
            return jsonify({"error": "Missing 'first' or 'last' query parameter"}), 400

        deleted_count = delete_guest_by_full_name_from_db(first_name, last_name)
        if deleted_count > 0:
            return jsonify({"message": f"{deleted_count} guest(s) named {first_name} {last_name} deleted"}), 200
        else:
            return jsonify({"message": f"No guests found with name {first_name} {last_name}"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete guest", "details": str(e)}), 500
    finally:
        print(f"DELETE /guests/by-full-name?last={last_name}&first={first_name} request processed.")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)