from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from datetime import datetime, date, time, timedelta
from db_utils import get_connection

load_dotenv() # Load env

app = Flask(__name__)


@app.route('/requestBooking', methods=['post'])
def requestBooking():
    requestJson = request.get_json()
    responseJson = {}
    
    # make datetime keys and put default times if no time specified
    defaultTimes = ("15:00:00", "11:00:00")
    if (requestJson.get("startTime") == None or not requestJson.get("startTime")):
        requestJson["startTime"] = defaultTimes[0]
    if (requestJson.get("endTime") == None or not requestJson.get("endTime")):
        requestJson["endTime"] = defaultTimes[1]
    
    # make db conn
    conn = get_connection()
    cursor = conn.cursor()

    # make query
    query = f"""
    SELECT roomMeta.*
    FROM roomMeta
    WHERE roomMeta.type = {requestJson['roomType']}
    AND NOT EXISTS (
        SELECT 1
        FROM roomBooking
        WHERE roomBooking.roomNr = roomMeta.roomNr
        AND '{requestJson["endDate"]} {requestJson["endTime"]}' > roomBooking.startTime
        AND '{requestJson["startDate"]} {requestJson["startTime"]}' < roomBooking.endTime
    );
    """ 
    
    cursor.execute(query)
    availableRooms = cursor.fetchall()
    
    # check if there is enouth space
    totalAvailableCapacity = sum(room[1] for room in availableRooms)

    if (totalAvailableCapacity > requestJson["peopleAmount"]):
        
        responseJson["approved"] = True

        bookedRooms = []
        bookedCapacity = 0
        i = 0

        # Her tager vi fat i de første og ikke dem som giver mest mening, det betyder at hvis der er 5 gæster og i samme kategori er der rum med 2 capasitet, men dem med 1 kapasitet har lavest roomNR for de dem, så 5 rum med 1 seng

        while(bookedCapacity < requestJson["peopleAmount"]):
            roomMap = {
                "roomNr": availableRooms[i][0],
                "capacity": availableRooms[i][2],
            }
            bookedRooms.append(roomMap)
            bookedCapacity += availableRooms[i][2]
            i += 1

        # add bookings to db
        for booking in bookedRooms:
            insertQuery = f"insert into roomBooking (roomNr, startTime, endTime) VALUES ({booking['roomNr']}, '{requestJson['startDate']} {requestJson['startTime']}', '{requestJson['endDate']} {requestJson['endTime']}');"
            cursor.execute(insertQuery)
            print(insertQuery)

        conn.commit()

        responseJson["rooms"] = bookedRooms
        responseJson["roomAmount"] = len(bookedRooms)

    else:
        responseJson["approved"] = False

    cursor.close()
    conn.close()

    return jsonify(responseJson)

@app.route('/testPost', methods=['post'])
def testPost():
    return "this also works!"

@app.route('/test', methods=['GET'])
def test():
    return "this works!!!!🦞🦞🥷🏿🦤🫎🏕️"


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0') # exposed port = 5002
