"""Mock implementations for hardware-specific modules when running on non-Raspberry Pi systems."""
import sys
from unittest.mock import MagicMock

class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0
    PUD_DOWN = "PUD_DOWN"
    
    @staticmethod
    def setmode(mode): print(f"GPIO: Set mode to {mode}")
    
    @staticmethod
    def setup(pin, mode, pull_up_down=None):
        args = [pin, mode]
        if pull_up_down: args.append(pull_up_down)
        print(f"GPIO: Setup pin {', '.join(str(x) for x in args)}")
    
    @staticmethod
    def output(pin, value): print(f"GPIO: Pin {pin} set to {value}")
    
    @staticmethod
    def input(pin): return 0  # Always return LOW for mock
    
    @staticmethod
    def cleanup(): print("GPIO: Cleanup called")
    
    class PWM:
        def __init__(self, pin, freq):
            self.pin = pin
            self.freq = freq
            print(f"PWM: Initialized on pin {pin} at {freq}Hz")
        
        def start(self, dc):
            print(f"PWM: Started on pin {self.pin} with duty cycle {dc}%")
        
        def stop(self):
            print(f"PWM: Stopped on pin {self.pin}")
        
        def ChangeFrequency(self, freq):
            self.freq = freq
            print(f"PWM: Changed frequency to {freq}Hz")

class MockSMBus:
    def __init__(self, bus):
        self.bus = bus
        print(f"SMBus: Initialized on bus {bus}")
    
    def write_byte_data(self, addr, cmd, val):
        print(f"SMBus: Write to address 0x{addr:02X}, cmd 0x{cmd:02X}, value 0x{val:02X}")

class MockBoard:
    """Mock implementation of DFRobot ADC board interface"""
    STA_OK = 0
    A0 = 0
    
    @staticmethod
    def begin():
        print("DFRobot ADC Board: Initialize")
        return 0  # STA_OK
    
    @staticmethod
    def set_adc_enable():
        print("DFRobot ADC Board: ADC enabled")
    
    @staticmethod
    def get_adc_value(pin):
        # Simulate distance readings in a realistic range
        # Returns values that will convert to distances between 5-30cm
        from random import randint
        return randint(300, 800)  # Will convert to ~5-30cm range

def board_detect():
    print("DFRobot ADC Board: Detection started")

def print_board_status():
    print("DFRobot ADC Board: Status check (mock implementation)")

# Create the mock board instance
board = MockBoard()