from flask import Flask, request, jsonify, render_template_string  # type: ignore
from flask_cors import CORS  # type: ignore

app = Flask(__name__)
CORS(app)

# Initial data for ESP32 and FLET systems
esp_data = {"light": 0, "motion": False}
flet_data = {
    "led": False,
    "fan_speed": 0,
    "led_override": False 
}

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Status</title>
    <meta http-equiv="refresh" content="1">
</head>
<body>
    <h1>ESP32 Monitor</h1>
    <div style="text-align: center;">
    <p style="color: green;"><strong> <<< Data from APP >>> </strong></p>
    <div style="text-align: left;">
    <p><strong> LED State:</strong> {{'ON' if flet_data['led'] else 'OFF' }}</p>
    <p><strong>Fan Speed:</strong> {{ flet_data['fan_speed']}}</p>
    <p><strong>LED Override:</strong> {{ 'Enabled' if flet_data['led_override'] else 'Disabled' }}</p>
    </div>
    <div style="text-align: center;">
    <p style="color: green;"><strong> <<< Data From ESP32 >>> </strong></p>
    <div style="text-align:left;">
    <p><strong>Light Level (0-100):</strong> {{ esp_data['light']}}</p>
    <p><strong>Motion:</strong> {{ 'Detected' if esp_data['motion'] else 'No Motion'}}</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, esp_data=esp_data, flet_data=flet_data)

@app.route('/esp/update', methods=['POST'])
def update_from_esp():
    data = request.json
    esp_data["light"] = data.get("light", 0)
    esp_data["motion"] = data.get("motion", False)
    return jsonify({"message": "ESP data received"}), 200


@app.route('/esp/control', methods=['GET'])#CONTROL DATA
def send_to_esp():
    return jsonify({
        "led": flet_data["led"],
        "fan_speed": flet_data["fan_speed"],
        "led_override": flet_data["led_override"]
    }), 200

@app.route('/flet/update', methods=['POST'])
def update_from_flet():
    data = request.json
    flet_data["led"] = data.get("led", False)
    flet_data["fan_speed"] = data.get("fan_speed", 0)
    flet_data["led_override"] = data.get("led_override", False) 
    return jsonify({"message": "FLET data received"}), 200

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return jsonify({"flet": flet_data, "esp": esp_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
