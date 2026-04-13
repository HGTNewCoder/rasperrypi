from gpiozero import Button
from signal import pause

# GPIO pin 11 (BCM numbering by default in gpiozero)
button = Button(11)

print("Testing GPIO Pin 11 - Press Ctrl+C to exit")
print("-" * 40)

def on_press():
    print("Pin 11: PRESSED")

def on_release():
    print("Pin 11: RELEASED")

# Assign event handlers
button.when_pressed = on_press
button.when_released = on_release

pause()  # Keep the script running