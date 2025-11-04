from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/postBooking', methods=['POST'])
def postBooking():
    
    bookingJson = request.get_json()
    returnJson = {}
    returnJson["approved"] = True

    # get room
    # request cleaning
    # post guest
    # 

    def bookRoom():
        requestBody = {
            "startDate": bookingJson.get("arrivalDate"),
            "endDate": bookingJson.get("departureDate"),
            "startTime": bookingJson.get("arivalTime"),
            "endTime": bookingJson.get("departuretime"),
            "peopleAmount": bookingJson.get("peopleAmount"),
            "roomType": bookingJson.get("roomType")
        }

        tempUrl = "http://localhost:5002/requestBooking" # skal ændres når container
        requestHeader = {'Content-Type': 'application/json'}

        response = requests.post(tempUrl, headers=requestHeader, json=requestBody)
        responseObj = response.json()

        if (not responseObj.get("approved")):
            returnJson["approved"] = False
            returnJson["message"] = "Error in room scheduling"
        else:
            bookingJson["rooms"] = responseObj.get("rooms")
            bookingJson["roomAmount"] = responseObj.get("roomAmount")
            print("succesfully booked room")

    def scheduleCleaning():
        None

    def informGuestService():
        requestBody = {
            "First Name": bookingJson.get("fName"), 
            "Last Name": bookingJson.get("lName"), 
            "Allergies": bookingJson.get("allergies"), 
            # "Bed Amount": bookingJson.get(""), -- not your buisness
            # "Type": bookingJson.get(""), -- not your buisness
            "Luggage": bookingJson.get("Luggage"), 
            "Additional Request": bookingJson.get("additionalRequest"), 
            # "Diet Request": bookingJson.get("") -- idkbro
            "isVIP": bookingJson.get("isVIP")
        }

        requestHeader = {'Content-Type': 'application/json'}
        tempUrl = "http://localhost:5000/guests" # skal ændres når container

        response = requests.post(tempUrl, headers=requestHeader, json=requestBody)
        responseObj = response.json()

        if(response != 201):
            returnJson["approved"] = False
            returnJson["message"] = "Error in guest creation"
            print("Error in guest creation")
        else:
            print("succesfully created guest")


    bookRoom()
    scheduleCleaning()
    return bookingJson

@app.route('/', methods=['GET'])
def test():
    url = "http://localhost:5002/test?"
    result = requests.get(url)
    return result
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")