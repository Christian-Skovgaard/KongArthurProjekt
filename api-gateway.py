from flask import Flask, request, jsonify
import mysql.connector

password_key = "your_password_here"

con=mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=password_key,
    database="hotel_kong_arthur",
)

app = Flask(__name__)

@app.route('/is-running')
def main():
    return "API Gateway is running"


@app.route('/getdrink/all', methods=['GET'])
def get_table_drink():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM drink")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    con.close()

    result = [dict(zip(columns, row)) for row in rows]

    return jsonify({"drinks": result}), 200


@app.route('/getdrink/type',methods=['GET'])
def get_table_drink_type():
    cursor=con.cursor()
    cursor.execute("SELECT * FROM drink")
    tables=cursor.fetchall()
    cursor.close()
    con.close()
    table_names=[table[0] for table in tables]
    return jsonify({"tables":table_names}),200


if __name__ == '__main__':
    print("Connecting to DB...")
    app.run(debug=True)