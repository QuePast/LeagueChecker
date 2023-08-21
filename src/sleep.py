import os
import time

def display_ascii_art_during_sleep(duration):
    frames = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
            print(frame)
            time.sleep(0.1)  # Adjust this value to change the speed of the animation

# Replace the sleep(1) in your code with:
display_ascii_art_during_sleep(1)