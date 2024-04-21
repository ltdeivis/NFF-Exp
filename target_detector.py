# Pip install method (recommended)
from IPython import display
display.clear_output()

# Old stuff
from PIL import ImageGrab
import time
import keyboard
import pyautogui
import numpy as np
import io

# ROBOFLOW / YOLO
from ultralytics import YOLO
from roboflow import Roboflow
from inference import get_model

from IPython.display import display, Image

#ultralytics.checks()

if __name__ == '__main__':
    print("Loading Model...")
    # ROBOFLOW
    rf = Roboflow(api_key="cqSyLbTH9bOTdZ5hqsz0")
    project = rf.workspace("mldatasets").project("nff-target")
    model = project.version(2).model

    # YOLOv8 Model
    #model = YOLO("./YoloV8Model/yolov8n.pt")

    # model = get_model(model_id=)
    # results = model.infer(image)
    
    # Search radius around the position
    radius = 175 # +- 300 == 600x600

    print("Starting main loop...")
    print("Press F7 to set position for detection")
    print("Press F5 to begin, or F6 to exit")

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
            
            # Screenshot loop
            while True:
                # Listen for stop signal
                if keyboard.is_pressed("q"):
                    print("Stopping target detector script...")
                    break


                # Take screenshot of area
                area_img = ImageGrab.grab(bbox=area)
                area_img.save("./player_dataset/img_1.jpg")

                # ROBOFLOW
                Results = model.predict("./player_dataset/img_1.jpg", confidence=40, overlap=30).json()

                if Results['predictions']:
                    prediction = Results['predictions'][0]

                    # Extracting the x and y values
                    x = prediction['x']
                    y = prediction['y']

                    screen_x, screen_y = (area[0] + x, area[1] + y)
                    pyautogui.moveTo(x=screen_x, y=screen_y)

                    print(f'{x}, {y}')
                else:
                    print("Nothing found")

                #results = model.predict(source=area_img, conf=0.3)
                #print(f"Results : {results[0].boxes.xyxy}")
                #time.sleep(0.4)

                #area_img.show()
                #break