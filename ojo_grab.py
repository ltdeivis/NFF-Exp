import pyautogui
import time
import keyboard
import win32gui
import win32con
import numpy as np
from multiprocessing import Process, Queue
from PIL import ImageGrab
from pynput.mouse import Listener

pyautogui.useImageNotFoundException()

# Draw rectangle on the screen
def draw_rectangle(x, y, width, height):
    hwnd = win32gui.GetDesktopWindow()
    hdc = win32gui.GetDC(hwnd)
    
    # Set brush style to NULL_BRUSH to not fill inside
    win32gui.SelectObject(hdc, win32gui.GetStockObject(win32con.NULL_BRUSH))

    # Define the rectangle coordinates
    left = x
    top = y
    right = x + width
    bottom = y + height
    
    # Draw the rectangle
    win32gui.Rectangle(hdc, left, top, right, bottom)
    
    # Release the device context
    win32gui.ReleaseDC(hwnd, hdc)

# Search around a given area for the detection_image and store found x/y to output_queue or None if not found
def player_search(detection_image, area, output_queue):
    try:
        area_img = ImageGrab.grab(bbox=area)
        Player = pyautogui.locate(needleImage=detection_image, haystackImage=area_img, grayscale=True, confidence=0.45)
        if Player != None:
            # Get center x/y of detection
            x, y = pyautogui.center(Player)
            # Add x,y as a tuple to the output
            output_queue.put((x,y))
        else:
            output_queue.put(None)
    except pyautogui.ImageNotFoundException:
        return output_queue.put(None)

def kill_processes(processes):
    for p in processes:
        p.kill()

def flicker_spam():
    while True:
        keyboard.press_and_release('1')
        time.sleep(1.3)

if __name__ == '__main__':
    # Search radius around the position
    radius = 250

    # Detect Front / Side / Back seperately
    num_processes = 3

    # Create output queue to retrieve output from processes
    # Output queue for each process
    output_queues = [Queue() for _ in range(num_processes)]

    # TODO: DEBUG
    #counter = 300
    sleep_time = 0.1

    x, y = 0, 0
    area = (0,0,0,0)

    print("Press F5 to start detecting or F6 to exit the script, F7 to set player position")

    # Main loop
    while True:
        time.sleep(0.5)
        if keyboard.is_pressed("F7"):
            # Get mouse location on screen and adjust the search radius2
            x, y = pyautogui.position()
            area = (np.min(x - radius,0), np.min(y - radius,0), x + radius, y + radius)
            print(f"Mouse position : {x}, {y}; area {area}")
        if keyboard.is_pressed("F6"):
            print("Closing script...")
            break
        if keyboard.is_pressed("F5"):
            print("Starting player detector script... Press hold Q to quit")

            f_spam = Process(target=flicker_spam, args=())
            f_spam.start()

            # Start loop to detect players around the mouse
            while True:
                # Create a player detector processes
                processes = []
                
                #print("Defining processes...")
                for i in range(num_processes):
                    p_detector = Process(target=player_search, args=(f"./target_{i}.png", area, output_queues[i]))
                    processes.append(p_detector)

                #print("Starting processes...")
                # Start detector processes
                for p in processes:
                    p.start()

                # Listen for stop signal
                if keyboard.is_pressed("q"):
                    print("Stopping player detector script...")
                    f_spam.kill()
                    kill_processes(processes)
                    break
            
                # Wait for processes to terminate
                #print("Joining processes...")
                for p in processes:
                    p.join()

                # Retrieve the results
                #print("Retrieving output...")
                #results = []
                for q in output_queues:
                    result = q.get()
                    if result != None:
                        # Press CHOKE DEM BITCHES
                        screen_x, screen_y = (area[0] + result[0], area[1] + result[1])
                        pyautogui.click(screen_x + 50, screen_y, clicks=2)
                        keyboard.press_and_release('5')
                        time.sleep(3)
                        keyboard.press_and_release('4')

                    #results.append(result)

                #print(f"Results found: {results}")
                
                # TODO: DEBUG
                # Run number restriction + sleep
                # counter = counter - 1
                # if counter <= 0:
                #     break
                #time.sleep(sleep_time)
            
            print("Script paused, press F5 to start detecting again or F6 to exit the script")
