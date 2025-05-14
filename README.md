# 🧠 Smart Room Controller (ESP32 + Flet + Flask)

This is a **Smart Room Controller** system that combines hardware and software to monitor and control environmental conditions in a room. It features:

- 📱 A Flet-based UI for real-time control of room devices
- 🌐 A Flask REST API backend that handles communication between UI and hardware
- 🔌 An ESP32 microcontroller that reads sensor data and controls actuators

---

## 📦 Features

- Toggle LED with manual or automatic override
- Control fan speed (0–255 PWM) via slider
- Monitor:
  - 💡 Ambient light level (0–100)
  - 🚶 Motion detection (PIR sensor)
- Web-based live status page
- Local API communication between ESP32, Flet, and Flask

Component	Description
ESP32	ESP32-WROVER	      Main microcontroller (Wi-Fi enabled)
P1	PIR Sensor      	    Detects motion
LDR + R3	            	  LDR + 10kΩ resistor forms a voltage divider
LED1, LED2    	          Simulate devices 
R1, R2	Resistors (100Ω)	Limit current for LEDs


---

## 🚀 Getting Started

### ✅ Prerequisites

- ESP32 board with sensors 
- Python 3.9+
- Arduino IDE with ESP32 board support
- Local Wi-Fi network (all devices must be on the same network)

---

1. Flash the ESP32

Upload the Arduino sketch named assaignment to your ESP32.

Make sure to:
- Update the IP address of the Flask server in the ESP code.
- Use a 10K + light-dependent resistor for light sensing.
- Use a PIR sensor for motion.

2. Run the Flask Server name backend
3. Run the flet app (main.py script contains the code of app)

4. Connect the circuit as follows


![image](https://github.com/user-attachments/assets/b8817888-1f6f-4ceb-84eb-f349a287610e)
