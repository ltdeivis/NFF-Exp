import pyautogui
import time
import keyboard
import numpy as np
from multiprocessing import Process, Queue
from PIL import ImageGrab

pyautogui.useImageNotFoundException()

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

if __name__ == '__main__':
    # Search radius around the mouse
    radius = 60

    # Detect Front / Side / Back seperately
    num_processes = 3

    # Create output queue to retrieve output from processes
    # Output queue for each process
    output_queues = [Queue() for _ in range(num_processes)]

    # TODO: DEBUG
    counter = 300
    sleep_time = 0.3

    #draw_rectangle(100, 100, 200, 200)

    print("Press F5 to start detecting or F6 to exit the script")

    # Main loop
    while True:
        if keyboard.is_pressed("F6"):
            print("Closing script...")
            break
        if keyboard.is_pressed("F5"):
            print("Starting player detector script... Press hold Q to quit")

            # Start loop to detect players around the mouse
            while True:
                # Get mouse location on screen and adjust the search radius2
                # TODO : Figure out monitor width/height to restrict end x/y to that so it doesnt try getting screenshot out of bounds of monitor
                x, y = pyautogui.position()
                area = (np.min(x - radius,0), np.min(y - radius,0), x + radius, y + radius)
                #print(f"Mouse position : {x}, {y}; area {area}")

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
                    # TODO : DEBUG
                    result = q.get()
                    if result != None:
                        # x,y is mouse position
                        # Radius will be applied to x,y to get a area
                        # result is the x,y from the area x,y
                        # To get draw location, need to relate result x,y with area x,y
                        screen_x, screen_y = (area[0] + result[0], area[1] + result[1])
                        pyautogui.click(screen_x + 50, screen_y, clicks=2)
                        keyboard.press_and_release('4')


                    #results.append(result)

                #print(f"Results found: {results}")
            
            print("Script paused, press F5 to start detecting again or F6 to exit the script")
