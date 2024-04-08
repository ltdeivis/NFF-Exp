import pyautogui
import time
import keyboard
from pynput.mouse import Listener
import numpy as np
from multiprocessing import Process

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

pyautogui.useImageNotFoundException()

def orb_click(OrbImage, Region):
    # Main loop
    while True:
        if keyboard.is_pressed('q'):
            print("Exit key pressed. Exiting loop.")
            break
        try:
            ExpOrbLoc = pyautogui.locateOnScreen(OrbImage, region=Region, grayscale=True, confidence=0.6)
            if ExpOrbLoc != None:
                x, y = pyautogui.center(ExpOrbLoc)
                print(f"Orb found : {x}, {y}")
                pyautogui.click(x=x, y=y)
                time.sleep(0.05)
        except pyautogui.ImageNotFoundException:
            continue

if __name__ == '__main__':
    # Draw rectangle and define the area
    start_x, start_y, end_x, end_y = draw_rectangle()
    area = (start_x, start_y, end_x, end_y)#

    # Divide the area into 2 to be used by processes
    w = np.abs(start_x - end_x)
    h = np.abs(start_y - end_y)
    a1 = (start_x, start_y, end_x, start_y + int(w * 0.55))
    a2 = (start_x, start_y + int(w * 0.45), end_x, end_y)

    # Start 2 processes that will scan for orbs (p1 has full size orb, p2 has slightly smaller orb)
    p1 = Process(target=orb_click, args=('./nff_exp_orb.png',a1,))
    p2 = Process(target=orb_click, args=('./nff_exp_orb2.png',a2,))

    # Star the threads
    p1.start()
    p2.start()

    p1.join()
    p2.join()