from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

#Database connection
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')
mysql.init_app(app)


# Get all cleaning tasks
@app.route('/cleaning/tasks', methods=['GET'])
def get_cleaning_tasks():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM hotel_arthur_cleaning_service;")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cleaning_tasks = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify(cleaning_tasks), 200

#Get cleaning task by room id
@app.route('/cleaning/room_number', methods=['GET'])
def get_cleaning_task_by_id():
    conn = mysql.connect()
    cursor = conn.cursor()

    room_number = request.args.get('room_number')
    cursor.execute("SELECT * FROM hotel_arthur_cleaning_service WHERE room_id = %s;", (room_number,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cleaning_tasks = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify(cleaning_tasks), 200


# Add new cleaning task - venter på Christian
@app.route('/cleaning/newtask', methods=['POST'])
def add_cleaning_task():
    task_data = request.json
    room_number = task_data.get()
    cleaning_task_completed[room_number] = {
        "task_status": False
    }
    return jsonify({"message": "Cleaning task added"}), 201


# Update cleaning task status
@app.route('/cleaning/<room_number>/changestatus', methods=['PUT'])
def update_cleaning_task_status(room_number):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Get current status
    cursor.execute("SELECT task_status FROM hotel_arthur_cleaning_service WHERE room_id = %s;", (room_number,))
    result = cursor.fetchone()
    
    if result is not None:
        current_status = bool(result[0])  # Convert to boolean
        new_status = not current_status  # Toggle between True and False
        
        # Update with new status
        cursor.execute("UPDATE hotel_arthur_cleaning_service SET task_status = %s WHERE room_id = %s;", (new_status, room_number))
        conn.commit()
        message = f"Cleaning task status updated to {new_status}"
        status_code = 200
    else:
        message = "Room not found"
        status_code = 404

    cursor.close()
    conn.close()
    return jsonify({"message": message}), status_code


# Remove room from cleaning tasks
@app.route('/cleaning/checkout/<room_number>', methods=['DELETE'])
def remove_room_from_cleaning_tasks(room_number):

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM hotel_arthur_cleaning_service WHERE room_id = %s;", (room_number,))
    
    conn.commit()  
    cursor.close()
    conn.close()
    return jsonify({"message": f"Room {room_number} removed from cleaning tasks"}), 200

app.run(debug=True, host='0.0.0.0', port=5000)