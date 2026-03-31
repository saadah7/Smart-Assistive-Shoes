👟 Smart Assistive Shoes – Mini Project

A Raspberry Pi-based **Smart Assistive Footwear System** designed to assist visually impaired individuals with obstacle detection. Using distance sensors, vibration motor, LEDs, sound alerts, and an LCD display, this shoe alerts users about nearby objects in real-time, improving safety and mobility.

---

## 🚀 Features

* 🔴 **Obstacle Detection** using analog distance sensor
* 💥 **Vibration Alerts** for close-range obstacles
* 🔊 **Mario Coin Sound** feedback via speaker
* 💡 **LED Indicators** based on object distance
* 🌈 **RGB Backlight** color-coded warnings
* 🔘 **Toggle System ON/OFF** using a push button

---

## ⚙️ Tech Stack

* **Hardware:**

  * Raspberry Pi (any model with GPIO + I2C)
  * DFROBOT Analog Distance Sensor (via `dfadc` library)
  * Vibration Motor
  * RGB Backlight Module
  * Buzzer/Speaker
  * LED
  * Push Button

* **Software:**

  * Python
  * RPi.GPIO
  * smbus2
  * dfadc (DFRobot ADC library)

---

## 🧠 How It Works

| Distance (cm) | Alert Mode  | RGB Color | Action                                      |
| ------------- | ----------- | --------- | ------------------------------------------- |
| `< 5`         | Danger Zone | 🔴 Red    | Vibrate, Flash LED, Play sound, LCD Warning |
| `5–10`        | Too Close   | 🟢 Green  | Vibrate, Flash LED, Double sound            |
| `10–15`       | Caution     | 🟠 Orange | Vibrate, LED blink, LCD Warning             |
| `> 15`        | All Clear   | 🔵 Blue   | No alerts                                   |

System can be toggled ON/OFF using the push button. RGB + LCD updates based on distance.

---

## 📦 Installation & Setup

1. **Enable I2C and GPIO** on Raspberry Pi (via `raspi-config`)
2. **Install dependencies:**

```bash
pip install RPi.GPIO smbus2
# Ensure dfadc is properly installed or copied into your project
```

3. **Wire all components** according to GPIO pin definitions:

| Component   | GPIO Pin                  |
| ----------- | ------------------------- |
| Vibration   | 17                        |
| LED         | 27                        |
| Speaker     | 18                        |
| Button      | 22                        |
| I2C Devices | SDA/SCL (Default Pi pins) |

4. **Run the script:**

```bash
python3 main.py
```

5. **Run as a Service** (Optional):
To automatically start the system on boot:
```bash
# Copy service file to systemd
sudo cp smart-shoes.service /etc/systemd/system/
# Reload systemd
sudo systemctl daemon-reload
# Enable the service
sudo systemctl enable smart-shoes
# Start the service
sudo systemctl start smart-shoes
# Check status
sudo systemctl status smart-shoes
```

## 🔧 Development Mode

The code includes mock implementations for non-Raspberry Pi development:
- Automatically detects if running on Pi or other system
- Uses mock GPIO, I2C, and ADC on non-Pi systems
- Prints debug information instead of accessing hardware
- Allows testing logic and UI flow without physical hardware

---

## 📷 Preview

> *GALLERY OF IMAGES*

---

## 🧑‍💻 Authors

👨‍💻 This project is developed by us as part of our Mini Project for Nawab Shah Alam Khan College of Engineering and Technology/ CSE Department.

* SAAD ABDUL HAKEEM - 161022733073
* M A NASER ASKARI - 161022733070
* SHAIKH MUSTAFA - 161022733068
....!!!
---

## 📜 License

This project is for educational purposes. Feel free to fork and improve!

that's a cool one