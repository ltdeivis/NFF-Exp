import pyautogui
import time
import keyboard
import win32gui
import win32con
import win32api
import numpy as np
from multiprocessing import Process, Queue
from PIL import ImageGrab
from pynput.mouse import Listener

import ctypes
from ctypes import windll

def get_default_set(x,y,w,h):
    # Top left, top right, bottom left, bottom right
    Pixels=[(x,y+1), (x+1,y+1), (x+2, y+1), (x,y+2), (x,y+3), 
            (x+w,y+1), (x+w-1,y+1), (x+w-2,y+1), (x+w,y+2), (x+w,y+3), 
            (x,y+h),(x,y+h-1),(x,y+h-2),(x+1,y+h),(x+2,y+h), 
            (x+w,y+h),(x+w-1,y+h),(x+w-2,y+h),(x+w,y+h-1),(x+w,y+h-2)]
    return Pixels

def get_transition_set(x,y,w,h):
    Pixels=[]
    return Pixels

# Take in SetDefault (static target), SetTransition (Spinning target) coordinate set
# e.g.: SetDefault=[(x1,y1), (x2,y2), ...], SetTransition=[...]
def target_check(Image, PixelSet):
    YellowPixels=0
    
    for PixelLoc in PixelSet:
        x, y = PixelLoc
        r, g, b = Image.getpixel((x,y))

        if np.abs(r - g) < 20 and (r > 200) and np.abs(g - b) > 120:
            YellowPixels+=1
        else:
            continue
        
        if YellowPixels > 10:
            return True
        else:
            continue
            
    return False


# Function to get coordinates of surounding tiles
# Including start tile
def get_surrounding_tiles(x, y, w, h, radius):
    surrounding_tiles = []
    # Loop over a range from -radius to radius for both x and y directions
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx * w  # Calculate new x-coordinate based on width
            ny = y + dy * h  # Calculate new y-coordinate based on height
            surrounding_tiles.append((nx, ny, dx, dy))
    return surrounding_tiles

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

if __name__ == '__main__':
    # Tile radius around user to search for
    radius=1

    print("Starting main loop...")
    print("Press F7 to draw position for character tile")
    print("Press F5 to begin, or F6 to exit")

    area=(0,0,0,0)

    # Main loop
    while True:
        time.sleep(0.5)
        if keyboard.is_pressed("F7"):
            # Draw rectangle where player tile is (Must make sure it's precise)
            start_x, start_y, end_x, end_y = draw_rectangle()
            area = (start_x, start_y, end_x, end_y)
            print(f"Area {area}")
        if keyboard.is_pressed("F6"):
            print("Closing script...")
            break
        if keyboard.is_pressed("F5"):
            if area==(0,0,0,1):
                print("Player tile missing, use F7 to select player tile")
                continue
            else:        
                print("Script started")        
                # Step 1 - Create tile array and work out surrounding tile coordinates
                # base_x, base_y, base_x2, base_y2 = area
                # base_w = np.abs(base_x - base_x2)
                # base_h = np.abs(base_y - base_y2)
                base_x, base_y, base_w, base_h = (694,516,43,43) # DAVID SCREEN SETUP
                Tiles=get_surrounding_tiles(base_x, base_y, base_w, base_h, radius)

                # DEBUG
                # Step 1b - Draw rectangles on screen for alanas
                DefaultSet=[]
                for Tile in Tiles:
                    tile_x, tile_y, dx, dy = Tile

                    # Step 3 - Workout for each tile where the 4 pixel regions are for target tile corners
                    Tile_DefaultSet = get_default_set(tile_x, tile_y, base_w, base_h)
                    TileInfo = (Tile_DefaultSet, tile_x, tile_y)
                    DefaultSet.append(TileInfo)

                    # Check target for each tile
                    #IsTarget = target_check(Tile_DefaultSet)
                    #print(f'TILE {tile_x}, {tile_y}, {base_w}, {base_h};  {dx}:{dy}; -- {IsTarget};  P={Part2Time}')


                    # Save image for DEBUG
                    #area_img.save(f'./player_dataset/img_{dx}_{dy}.jpg')


                # Step 2 - Workout tile pixel to game pixel (game is 32x32, scaled to monitor might be bigger like 65x65...)
                tile_center_x = base_w / 2
                tile_center_y = base_h / 2

                KeepRunning=True

                while KeepRunning:
                    # DBEUG
                    # keyboard.press_and_release('1')

                    # Take screenshot
                    Image = ImageGrab.grab()

                    # Check every tile target regions and do shit once found
                    for TileInfo in DefaultSet:
                        TileSet, x, y = TileInfo
                        if target_check(Image, TileSet):
                            keyboard.press_and_release('5')
                            time.sleep(5.65)
                            keyboard.press_and_release('4')

                            # TODO : If ojo grab used, wait for rough cooldown before using again
                            # Meanwhile use instant jutsu instead like taijutsu / normal grab (since it has lower cd)
                            # choose random move from a instant move set/array to use

                            #KeepRunning=False
                            break

    
    print("Script closed")