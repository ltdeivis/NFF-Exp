import pyautogui
import time
import keyboard
from pynput.mouse import Listener
import numpy as np
from multiprocessing import Process
from PIL import ImageGrab

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

def kill_processes(processes):
    for p in processes:
        p.kill()

def orb_click(OrbImage, area):
    while True:
        try:
            area_img = ImageGrab.grab(bbox=area)
            ExpOrbLoc = pyautogui.locate(needleImage=OrbImage, haystackImage=area_img, grayscale=True, confidence=0.6)
            if ExpOrbLoc != None:
                x, y = pyautogui.center(ExpOrbLoc)
                print(f"Orb found : {x}, {y}, {area}")
                pyautogui.click(x=x + area[0], y=y + area[1])
                time.sleep(0.04)
        except pyautogui.ImageNotFoundException:
            continue

if __name__ == '__main__':
    # Draw rectangle and define the area
    start_x, start_y, end_x, end_y = draw_rectangle()
    area = (start_x, start_y, end_x, end_y)

    # Divide the area into 2 to be used by processes
    w = np.abs(start_x - end_x)
    h = np.abs(start_y - end_y)
    a1 = (start_x, start_y, end_x, start_y + int(w * 0.55))
    a2 = (start_x, start_y + int(w * 0.45), end_x, end_y)

    sleep_time = 0.5

    print("Press F5 to start detecting or F6 to exit the script")

    # Main loop
    while True:
        if keyboard.is_pressed("F6"):
            print("Closing script...")
            break
        if keyboard.is_pressed("F5"):
            print("Starting player detector script... Press hold Q to quit")

            # Create a orb detector processes
            processes = []
            
            print("Defining processes...")
            p1 = Process(target=orb_click, args=(f"./nff_exp_orb.png", a1))
            p2 = Process(target=orb_click, args=(f"./nff_exp_orb2.png", a2))
            processes.append(p1)
            processes.append(p2)

            print("Starting processes...")
            # Start detector processes
            for p in processes:
                p.start()

            # Start loop
            while True:
                # Listen for stop signal
                if keyboard.is_pressed("q"):
                    print("Stopping player detector script...")
                    kill_processes(processes)
                    
                    # Wait for processes to terminate
                    print("Joining processes...")
                    for p in processes:
                        p.join()
                    break
                
                # Sleep inbetween detections
                time.sleep(sleep_time)
            
            print("Script paused, press F5 to start detecting again or F6 to exit the script")
