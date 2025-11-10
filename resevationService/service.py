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

        url = "http://roomschedulingservice:5000/requestBooking"
        tempUrl = "http://localhost:5000/requestBooking" # skal ændres når container
        requestHeader = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=requestHeader, json=requestBody)
        print(response)
        responseObj = response.json()

        if (not responseObj.get("approved")):
            returnJson["approved"] = False
            returnJson["message"] = "Error in room scheduling"
        else:
            bookingJson["rooms"] = responseObj.get("rooms")
            bookingJson["roomAmount"] = responseObj.get("roomAmount")
            print("succesfully booked room")

    def scheduleCleaning():
        i = 0
        while(i < len(bookingJson.get("rooms"))):
            requestObj = {
                "room_number": bookingJson.get("rooms")[i],
                "startDate": bookingJson.get("arrivalDate"),
                "endDate": bookingJson.get("departureDate")
            }

        url = "http://cleaningservice:5000/cleaning/newtask"
        header = {'Content-Type': 'application/json'}

        response = requests.post(url=url, headers=header, json=requestObj)
        if (response != 201):
            print("error in requesting cleaning: ", response)

    def informGuestService():
        requestBody = {
            "First Name": bookingJson.get("fName"), 
            "Last Name": bookingJson.get("lName"), 
            "Allergies": bookingJson.get("allergies"), 
            # "Bed Amount": bookingJson.get(""), -- not your buisness
            "Type": bookingJson.get("guestType"),
            "Luggage": bookingJson.get("Luggage"), 
            "Additional Request": bookingJson.get("additionalRequest"), 
            # "Diet Request": bookingJson.get("") -- idkbro
        }

        requestHeader = {'Content-Type': 'application/json'}
        tempUrl = "http://guestservice:5000/guests" # skal ændres når container

        response = requests.post(tempUrl, headers=requestHeader, json=requestBody)
        responseObj = response.json()

        # Vil gerne have et guestID med tilbage!!!

        if(response != 201):
            returnJson["approved"] = False
            returnJson["message"] = "Error in guest creation"
            print("Error in guest creation")
        else:
            print("succesfully created guest")

    print("booking")
    bookRoom()
    print("booking done")
    # scheduleCleaning()
    return returnJson

@app.route('/', methods=['GET'])
def test():
    print("testen🥷🏿")
    url = "http://roomschedulingservice:5000/test"
    result = requests.get(url)
    return result.text
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0") # exposed port = 5001