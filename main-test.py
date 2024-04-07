from PIL import ImageGrab
import numpy as np
import time
import pyautogui
from pynput.mouse import Listener

# For debug
import matplotlib.pyplot as plt

# TODO : Somehow this function isn't stopping red 'miss' text from being clicked
# Function to check if region contains white / red
def contains_white_or_red(region):
    # RGB Thresholds
    white_threshold = 185
    red_threshold = 150

    # Extract red and green channels
    red_channel = region[:,:,0]
    green_channel = region[:,:,1]
    blue_channel = region[:,:,2]

    # Check if any pixel is white or red
    #white_pixels = (red_channel > white_threshold) & (green_channel > white_threshold) & (blue_channel > white_threshold)
    #red_pixels = (red_channel > red_threshold) & (green_channel < 64) & (blue_channel < 45)
    
    rp = False
    
    x_shape, y_shape = red_channel.shape
    for x in range(x_shape):
        for y in range(y_shape):
            r_px = red_channel[x, y]
            g_px = green_channel[x, y]
            b_px = blue_channel[x, y]

            # For white check
            rg_df = np.abs(r_px - g_px)
            rb_df = np.abs(r_px - b_px)
            if not (rg_df > 15 or rb_df > 15):
                rp = True
                break

            #print(f"rgb=({r_px},{g_px},{b_px})")
            if ((r_px - g_px) > 95) and ((r_px - b_px) > 95):
                if r_px > 120 and g_px < 85 and b_px < 85:
                    rp = True
                    break
        if rp:
            print("rp true")
            break
        else:
            print("rp false")

    return rp

# TODO : Experimental red only detect
def detect_red(region, red_threshold=100, green_threshold=50, blue_threshold=50):
    """
    Detects if an region contains any shade of red.
    
    Parameters:
    region (numpy.ndarray): RGB region array with shape (height, width, 3).
    red_threshold (int): Threshold for the red channel.
    green_threshold (int): Threshold for the green channel.
    blue_threshold (int): Threshold for the blue channel.

    Returns:
    bool: True if red is detected, False otherwise.
    """
    red_pixels = np.logical_and.reduce((
        region[:, :, 0] > red_threshold,
        region[:, :, 0] > region[:, :, 1] + green_threshold,
        region[:, :, 0] > region[:, :, 2] + blue_threshold
    ))
    return np.any(red_pixels)

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

# pixel search radius
radius = 10

# Step size for search
step_size = 18

# Click adjustment
click_offset = 8

# Last clicked region
last_x = 0
last_y = 0
last_x_radius = 20
last_y_radius = 40

while True:
    # Capture initial screenshot
    initial_screenshot = ImageGrab.grab(bbox=area)
    initial_array = np.array(initial_screenshot)

    # Wait a bit (40fps - processing)
    time.sleep(0.025)

    # Capture the current screenshot of the defined area
    current_screenshot = ImageGrab.grab(bbox=area)
    current_array = np.array(current_screenshot)

    change_found = False

    # Compare the initial screenshot with the current one by sampling pixels
    for x in range(0, initial_array.shape[1], step_size):
        for y in range(0, initial_array.shape[0], step_size):
            # Get the pixel at (x, y) in both images
            if is_within_bounds(y + radius, x + radius, initial_array):
                if (y < last_y - last_y_radius or y > last_y + last_y_radius) and (x < last_x - last_x_radius or x > last_x + last_x_radius):
                    # Get a range of pixels radius x radius
                    initial_pixel_range = initial_array[y:y+radius, x:x+radius]
                    current_pixel_range = current_array[y:y+radius, x:x+radius]

                    unequal_elements = initial_pixel_range != current_pixel_range

                    if np.all(unequal_elements):
                        #if contains_white_or_red(current_pixel_range):
                        if detect_red(current_pixel_range):
                            print("Contains red/white")
                            break
                        print(f"Pixel threshold reached at ({x}, {y})")
                        #pyautogui.moveTo(start_x + x + click_offset, start_y + y + click_offset)
                        pyautogui.click(x=start_x + x + click_offset, y=start_y + y + click_offset)
                        #pyautogui.moveTo(10,10)
                        last_x = x
                        last_y = y
                        change_found = True
                        break
        if change_found:
            break
