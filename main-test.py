from PIL import ImageGrab
import numpy as np
import time
import pyautogui
from pynput.mouse import Listener

# For debug
import matplotlib.pyplot as plt

# Function to check if region contains white / red
def contains_white_or_red(region):
    # RGB Thresholds
    white_threshold = 185
    red_threshold = 120

    # Extract red and green channels
    red_channel = region[:,:,0]
    green_channel = region[:,:,1]
    blue_channel = region[:,:,2]

    # Check if any pixel is white or red
    white_pixels = (red_channel > white_threshold) & (green_channel > white_threshold) & (blue_channel > white_threshold)
    red_pixels = (red_channel > red_threshold) & (green_channel < 20) & (blue_channel < 20)
        
    return np.any(white_pixels) or np.any(red_pixels)

# Function to check if x and y are within np array of shape (y, x, ...) bounds
def is_within_bounds(y, x, np_array):
    if 0 <= y < np_array.shape[0] and 0 <= x < np_array.shape[1]:
        return True
    else:
        return False

# Function to draw a rectangle on the screen
def draw_rectangle():
    print("Please click and hold the mouse to start drawing the rectangle.")
    print("Release the mouse button to finish drawing.")

    start_x, start_y, end_x, end_y = None, None, None, None

    def on_click(x, y, button, pressed):
        nonlocal start_x, start_y
        nonlocal end_x, end_y
        print(f"On click {x} {y} {pressed}") # DEBUG
        if pressed:
            # Mouse key pressed
            print("The mouse key has held down")
            start_x, start_y = x, y

        if not pressed:
            # Mouse key released
            print("The mouse key has been released")
            end_x, end_y = x, y
            return False

    # Open Listener for mouse key presses
    with Listener(on_click=on_click) as listener:
        # Listen to the mouse key presses
        listener.join()

    # Ensure start coordinates are smaller than end coordinates
    start_x, end_x = min(start_x, end_x), max(start_x, end_x)
    start_y, end_y = min(start_y, end_y), max(start_y, end_y)

    return start_x, start_y, end_x, end_y

# Draw rectangle and define the area
start_x, start_y, end_x, end_y = draw_rectangle()
area = (start_x, start_y, end_x, end_y)

# Get the initial screenshot of the defined area
initial_screenshot = ImageGrab.grab(bbox=area)
initial_array = np.array(initial_screenshot)
#initial_screenshot.show()

# Sleep amount (15fps)
sleep_amount = 1 / 5

# pixel search radius
radius = 16

# Click adjustment
click_offset = 10

# Last clicked region
last_x = 0
last_y = 0
last_xy_radius = 20

print(f"DEBUG 1 : screenshot array shape - {initial_array.shape}")



while True:
    # Capture initial screenshot
    initial_screenshot = ImageGrab.grab(bbox=area)
    initial_array = np.array(initial_screenshot)

    # Wait a bit
    time.sleep(0.03)

    # Capture the current screenshot of the defined area
    current_screenshot = ImageGrab.grab(bbox=area)
    current_array = np.array(current_screenshot)

    change_found = False

    # Compare the initial screenshot with the current one by sampling pixels
    for x in range(0, initial_array.shape[1], radius):
        for y in range(0, initial_array.shape[0], radius):
            # Get the pixel at (x, y) in both images
            if is_within_bounds(y + radius, x + radius, initial_array):
                if (y < last_y - last_xy_radius or y > last_y + last_xy_radius) and (x < last_x - last_xy_radius or x > last_x + last_xy_radius):
                    # Get a range of pixels radius x radius
                    initial_pixel_range = initial_array[y:y+radius, x:x+radius]
                    current_pixel_range = current_array[y:y+radius, x:x+radius]

                    unequal_elements = initial_pixel_range != current_pixel_range

                    if np.all(unequal_elements) and not contains_white_or_red(current_pixel_range):
                        print(f"Pixel threshold reached at ({x}, {y})")
                        pyautogui.moveTo(start_x + x + click_offset, start_y + y + click_offset)
                        pyautogui.click()
                        pyautogui.moveTo(10,10)
                        last_x = x
                        last_y = y
                        change_found = True
                        break
        if change_found:
            break
