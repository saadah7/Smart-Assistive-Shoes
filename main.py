import platform
import time

# Use real hardware on Raspberry Pi, mock implementations elsewhere
if platform.machine().startswith('arm'):
    from dfadc import *
    import RPi.GPIO as GPIO
    from smbus2 import SMBus
else:
    print("Not running on Raspberry Pi - using mock implementations")
    from mock_hardware import MockGPIO as GPIO
    from mock_hardware import MockSMBus as SMBus
    from mock_hardware import board, board_detect

# === GPIO Pins ===
VIBRATION_PIN = 17
LED_PIN = 27
SPEAKER_PIN = 18
BUTTON_PIN = 22  # Push button GPIO

# === I2C LCD Constants ===
LCD_ADDRESS = 0x3E  # LCD I2C address
RGB_ADDRESS = 0x2D  # RGB backlight I2C address
bus = SMBus(1)

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBRATION_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

speaker_pwm = GPIO.PWM(SPEAKER_PIN, 440)

# === LCD Functions ===
def lcd_write(cmd, mode=0):
    try:
        bus.write_byte_data(LCD_ADDRESS, mode, cmd)
    except IOError as e:
        print(f"Error communicating with LCD: {e}")

def lcd_init():
    time.sleep(0.1)
    lcd_write(0x33)
    lcd_write(0x32)
    lcd_write(0x28)
    lcd_write(0x0C)
    lcd_write(0x06)
    lcd_write(0x01)
    time.sleep(0.1)

def lcd_set_text(text):
    lcd_write(0x01)
    time.sleep(0.1)
    row = 0
    count = 0
    for char in text:
        if char == '\n':
            row += 1
            count = 0
            if row == 1:
                lcd_write(0xC0)
        else:
            bus.write_byte_data(LCD_ADDRESS, 0x40, ord(char))
            count += 1
            if count == 16 and row == 0:
                lcd_write(0xC0)
                row += 1

# === RGB Backlight Functions ===
def set_rgb(r, g, b):
    try:
        print(f"Setting RGB to: R={r}, G={g}, B={b}")
        bus.write_byte_data(RGB_ADDRESS, 0x00, 0x00)
        bus.write_byte_data(RGB_ADDRESS, 0x01, 0x00)
        bus.write_byte_data(RGB_ADDRESS, 0x08, 0xaa)
        bus.write_byte_data(RGB_ADDRESS, 0x04, r)
        bus.write_byte_data(RGB_ADDRESS, 0x03, g)
        bus.write_byte_data(RGB_ADDRESS, 0x02, b)
    except IOError as e:
        print(f"Error communicating with RGB backlight: {e}")

# === Mario Coin Sound ===
def play_tone(freq, duration):
    speaker_pwm.ChangeFrequency(freq)
    speaker_pwm.start(50)
    time.sleep(duration)
    speaker_pwm.stop()

def play_mario_coin():
    play_tone(1318, 0.15)  # E6
    time.sleep(0.05)
    play_tone(1568, 0.15)  # G6

# === ADC Setup ===
board_detect()
while board.begin() != board.STA_OK:
    print_board_status()
    print("Board begin failed")
    time.sleep(2)
print("Board begin success")

board.set_adc_enable()
distance_threshold = 15  # cm

# Initialize LCD and RGB
lcd_init()
set_rgb(0, 128, 64)
lcd_set_text("System Ready")

# === System toggle state ===
system_enabled = True
last_button_state = GPIO.LOW

try:
    while True:
        # Toggle system state via push button
        button_state = GPIO.input(BUTTON_PIN)
        if button_state == GPIO.HIGH and last_button_state == GPIO.LOW:
            system_enabled = not system_enabled
            if system_enabled:
                lcd_set_text("System Enabled")
                set_rgb(0, 128, 64)  # greenish
            else:
                lcd_set_text("System Paused")
                set_rgb(255, 255, 0)  # yellow
            time.sleep(0.3)  # debounce
        last_button_state = button_state

        if not system_enabled:
            time.sleep(0.1)
            continue

        val = board.get_adc_value(board.A0)
        print("Raw ADC Value:", val)

        dist = val * 1276 / (1023.0 * 4) / 4 * 2.5
        dist = round(dist)
        print("Distance:", dist, "cm")

        # === Conditional Alerts Based on Distance ===
        if dist < 5:
            print("ð¨ Object extremely close!")
            GPIO.output(VIBRATION_PIN, GPIO.HIGH)
            for _ in range(5):
                GPIO.output(LED_PIN, GPIO.HIGH)
                play_mario_coin()
                time.sleep(0.1)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.1)
            lcd_set_text("Too Close!\nDanger Zone")
            set_rgb(255, 0, 0)  # Red
            GPIO.output(VIBRATION_PIN, GPIO.LOW)

        elif dist < 10:
            print("â ï¸ Object very close!")
            GPIO.output(VIBRATION_PIN, GPIO.HIGH)
            for _ in range(3):
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(0.15)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.15)
            play_mario_coin()
            time.sleep(0.1)
            play_mario_coin()
            lcd_set_text("Object too near\nBack off!")
            set_rgb(0, 255, 0)  # Green
            GPIO.output(VIBRATION_PIN, GPIO.LOW)

        elif dist < 15:
            print("â ï¸ Object approaching.")
            GPIO.output(VIBRATION_PIN, GPIO.HIGH)
            for _ in range(2):
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.2)
            play_mario_coin()
            lcd_set_text("Object Ahead\nCaution")
            set_rgb(255, 165, 0)  # Orange
            GPIO.output(VIBRATION_PIN, GPIO.LOW)

        else:
            GPIO.output(VIBRATION_PIN, GPIO.LOW)
            GPIO.output(LED_PIN, GPIO.LOW)
            lcd_set_text("Distance OK\nAll Clear")
            set_rgb(0, 0, 255)  # Blue

        time.sleep(2)

except KeyboardInterrupt:
    print("User interrupted")

finally:
    speaker_pwm.stop()
    GPIO.cleanup()
    lcd_write(0x01)
    lcd_set_text("System Stopped\n")
    set_rgb(0, 0, 0)
    print("GPIO cleaned up.")
