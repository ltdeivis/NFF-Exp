import pyautogui
import time
import keyboard
import numpy as np
from multiprocessing import Process
from PIL import ImageGrab
from pynput.mouse import Listener

# ====== Skill Keybinds =======

# -- CLAN KEYBINDS --
WebShotKey='p'
MultiWebShotKey='alt+o'
WebMazeKey='ctrl+o'
StickyKunaiKey='ctrl+i'

# -- Sub Job Keybindings --
GatheringLocationKey='l'
EyeOfKaguraKey='shift+l'

# -- TAI KEYBINDS --
NormalGrabKey='shift+p'
LeafWhirlWindKey='ctrl+p'
LeafViolentWindKey='alt+p'
LeafRisingWindKey='o'
LeafGreatWhirlWindKey='alt+k'
LeafDynamicEntry='u'
LeafGreatLightRotation='shift+k'
RockSmashKey='ctrl+k'

# -- NIN KEYBINDS --
BoulderKey='shift+o'
EarthWallKey='shift+u'
SwampUnderworldKey='ctrl+u'
SwampBramblesKey='alt+u'
RiverKey='ctrl+j'
AntLionKey='alt+j'
MoveStopperSettings=('j', 40)
PlanetaryOrbKey='alt+l'
EarthDragonKey='ctrl+l'
StoneDragonKey='m'

# -- SPAM KEYBINDS --
FlickerSettings=('i', 1) # every 2s
FlickerSettings=('i', 1) # every 2s
# - TOGLE -
CloneTrickSettings=('shift+i', 8) # every 8s
CloneSettings=('k', 10)        # every 10s
GatheringLocationSettings=('l', 14)  

# -- GENERAL KEYBINDS --
BlockKey='x'
StruggleKey='b'
PunchKey='space'
AlternateJutsu='r' # Some jutsus have different forms when alternate key is held while using the jutsu key

def get_default_set(x,y,w,h):
    # Top left, top right, bottom left, bottom right
    Pixels=[(x,y), (x+1,y), (x+2, y), (x,y+1), (x,y+2), 
            (x+w-1,y), (x+w-2,y), (x+w-3,y), (x+w-1,y+1), (x+w-1,y+2), 
            (x,y+h),(x,y+h-1),(x,y+h-2),(x+1,y+h),(x+2,y+h), 
            (x+w-1,y+h),(x+w-2,y+h),(x+w-3,y+h),(x+w-1,y+h-1),(x+w-1,y+h-2)]
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

def move_spam_thread():
    global CloneTrickSettings
    global CloneSettings
    global GatheringLocationSettings
    global MoveStopperSettings

    CloneTrickKey, CloneTrickCD = CloneTrickSettings
    CloneKey, CloneCD = CloneSettings
    GatheringKey, GatheringCD = GatheringLocationSettings
    MoveStopperKey, MoveStopperCD = MoveStopperSettings

    CloneTrickLastUsed=0
    CloneLastUsed=0
    GatheringLastUsed=0
    MoveStopperLastUsed=0

    print("MoveSpammer: thread started")

    while True:
        if (time.time() - CloneTrickLastUsed) > CloneTrickCD:
            keyboard.press_and_release(CloneTrickKey)
            CloneTrickLastUsed = time.time()
            time.sleep(0.05)
        if (time.time() - CloneLastUsed) > CloneCD:
            keyboard.press_and_release(CloneKey)
            CloneLastUsed = time.time()
            time.sleep(0.05)
        if (time.time() - GatheringLastUsed) > GatheringCD:
            keyboard.press_and_release(GatheringKey)
            GatheringLastUsed = time.time()
            time.sleep(0.05)
        if (time.time() - MoveStopperLastUsed) > MoveStopperCD:
            keyboard.press_and_release(MoveStopperKey)
            MoveStopperLastUsed = time.time()
            time.sleep(0.05)
        
        time.sleep(1)

def flicker_spam_thread():
    global FlickerSettings

    FlickerKey, FlickerCD = FlickerSettings

    print("FlickerSpammer: thread started")

    while True:
        keyboard.press_and_release(FlickerKey)
        time.sleep(FlickerCD)

def teleport_and_spike():
    # Double click -> Block -> Single spike
    pyautogui.click(clicks=2)
    time.sleep(0.02)
    keyboard.press_and_release(PunchKey)
    time.sleep(0.02)
    keyboard.press_and_release(MultiWebShotKey)
    time.sleep(0.02)
    keyboard.press_and_release(MultiWebShotKey)

def dagger_slash_combo():
    keyboard.press_and_release(PunchKey)
    time.sleep(0.01)
    keyboard.press_and_release(PunchKey)
    time.sleep(0.01)
    keyboard.press_and_release(PunchKey)
    time.sleep(0.01)

def alternate_jutsu(JutsuKey):
    keyboard.press(AlternateJutsu)
    keyboard.press_and_release(JutsuKey)
    time.sleep(0.05)
    keyboard.release(AlternateJutsu)

def flicker_block_jutsu(JutsuKey):
    pyautogui.click(clicks=2)
    time.sleep(0.02)
    keyboard.press_and_release(PunchKey)
    time.sleep(0.02)
    keyboard.press_and_release(JutsuKey)
    time.sleep(0.02)
    keyboard.press_and_release(JutsuKey)


if __name__ == '__main__':
    KeepRunning=True

    # MOVE SPAM PROCESS
    MoveSpammer=Process(target=move_spam_thread)
    IsMoveSpammerOn=False
    
    # FLICKER SPAM PROCESS
    FlickerSpammer=Process(target=flicker_spam_thread)
    IsFlickerSpammerOn=False

    # ======= MOVE ROTATION ARRAYS =========
    # Single item in list : (Fun, Args as dict)
    # For keypresses, Fun - keyboard.press_and_release, Args = {'hotkey': Keybind}
    # For MouseClicks, Fun - pyautogui.click, args={'x': X, 'y': Y, 'clicks': 2}
    # for func, kwargs in list:
    #   func(**kwargs)

    # AOE Spike ->  DoubleClick + Block + SingleSpike -> ColumnSpike
    SpikeCombo=[0, (teleport_and_spike,{}), (keyboard.press_and_release, {'hotkey' : EarthDragonKey}), (flicker_block_jutsu, {'JutsuKey': StoneDragonKey})]
    SpikeComboCounter=1
    SpikeMaxComboCounter=len(SpikeCombo)-1

    # Ojou grab off cd, index 0 is ojou cd, the rest are random moves to use
    MeleeCombo=[0, (keyboard.press_and_release, {'hotkey' : RockSmashKey}), (keyboard.press_and_release, {'hotkey': LeafWhirlWindKey}), 
                   (keyboard.press_and_release, {'hotkey': LeafViolentWindKey}), (keyboard.press_and_release, {'hotkey': NormalGrabKey}),
                   (keyboard.press_and_release, {'hotkey': LeafRisingWindKey}), (keyboard.press_and_release, {'hotkey': LeafGreatWhirlWindKey}), 
                   (keyboard.press_and_release, {'hotkey': LeafGreatLightRotation}), (keyboard.press_and_release, {'hotkey': LeafDynamicEntry}), 
                   (keyboard.press_and_release, {'hotkey': MultiWebShotKey})]
    MeleeComboCounter=1
    MeleeComboMaxCounter=len(MeleeCombo)-1

    # Aoe / CC moves
    AoeCombo=[0, (flicker_block_jutsu, {'JutsuKey' : PlanetaryOrbKey}), (flicker_block_jutsu, {'JutsuKey': SwampUnderworldKey}), 
                 (flicker_block_jutsu, {'JutsuKey': RiverKey}), (flicker_block_jutsu, {'JutsuKey': SwampBramblesKey})]
    AoeComboCounter=1
    AoeComboMaxCounter=len(AoeCombo)-1

    # Instant combo chain
    InstantCombo=[0, (flicker_block_jutsu, {'JutsuKey' : AntLionKey})]

    # On key release events
    def on_key_release(event):
        if event.name == 'e':
            global SpikeCombo
            global SpikeComboCounter
            global SpikeMaxComboCounter

            # Check time
            if (time.time() - SpikeCombo[0]) > 5.0:
                SpikeComboCounter = 1

            if SpikeComboCounter > SpikeMaxComboCounter:
                SpikeComboCounter = 1

            fun, kwargs = SpikeCombo[SpikeComboCounter]
            fun(**kwargs)
            time.sleep(0.03)
            fun(**kwargs)
            SpikeComboCounter+=1
            SpikeCombo[0] = time.time()
        elif event.name == 'g':
            global IsMoveSpammerOn
            global MoveSpammer
            if IsMoveSpammerOn:
                print("MoveSpammer: Killing thread")
                MoveSpammer.kill()
                MoveSpammer.join()
            else:
                print("MoveSpammer: starting thread")
                MoveSpammer=Process(target=move_spam_thread)
                MoveSpammer.start()
            IsMoveSpammerOn=not IsMoveSpammerOn
        elif event.name == 'h':
            global IsFlickerSpammerOn
            global FlickerSpammer
            if IsFlickerSpammerOn:
                print("FlickerSpammer: Killing thread")
                FlickerSpammer.kill()
                FlickerSpammer.join()
            else:
                print("FlickerSpammer: starting thread")
                FlickerSpammer=Process(target=flicker_spam_thread)
                FlickerSpammer.start()
            IsFlickerSpammerOn=not IsFlickerSpammerOn
        elif event.name == 'f':
            global AoeCombo
            global AoeComboCounter
            global AoeComboMaxCounter

            if AoeComboCounter > AoeComboMaxCounter:
                AoeComboCounter = 1

            fun, kwargs = AoeCombo[AoeComboCounter]
            fun(**kwargs)
            time.sleep(0.03)
            fun(**kwargs)
            AoeComboCounter+=1
            AoeCombo[0] = time.time()
        elif event.name == 'q':
            global InstantCombo

            # Check last used over 30s
            if time.time() - InstantCombo[0] > 30:
                # First do flicker punch
                pyautogui.click(clicks=2)
                time.sleep(0.01)
                keyboard.press_and_release(PunchKey)
                time.sleep(0.01)

                for Combo in InstantCombo[1:]:
                    fun, kwargs = Combo
                    fun(**kwargs)
                    time.sleep(0.03)
                    fun(**kwargs)
                    InstantCombo[0] = time.time()
        elif event.name == 'f4':
            global KeepRunning
            print("Pausing script... Press F5 to start the script again")
            KeepRunning = not KeepRunning


    # hook to all key release events
    keyboard.on_release(on_key_release)

    # Tile radius around user to search for
    radius=1
    pyautogui.click()
    print("Starting main loop...")
    print("Press F7 to draw position for character tile")
    print("Press F5 to begin, or F6 to exit")

    area=(0,0,0,0)

    # Main loop
    while True:
        time.sleep(0.5)
        if keyboard.is_pressed("F6"):
            print("Closing script...")
            break
        if keyboard.is_pressed("F5"):
            print("Script started")    
            KeepRunning = True    
            # Step 1 - Create tile array and work out surrounding tile coordinates
            base_x, base_y, base_w, base_h = (694,520,43,43) # DAVID SCREEN SETUP
            Tiles=get_surrounding_tiles(base_x, base_y, base_w, base_h, radius)

            DefaultSet=[]
            for Tile in Tiles:
                tile_x, tile_y, dx, dy = Tile

                # Step 3 - Workout for each tile where the 4 pixel regions are for target tile corners
                Tile_DefaultSet = get_default_set(tile_x, tile_y, base_w, base_h)
                TileInfo = (Tile_DefaultSet, tile_x, tile_y)
                DefaultSet.append(TileInfo)

            #     area_img = ImageGrab.grab(bbox=(tile_x, tile_y, tile_x + base_w, tile_y + base_h))
                
            #     Image = ImageGrab.grab()
            #     IsTarget = target_check(Image, Tile_DefaultSet)

            #     print(f'TILE {tile_x}, {tile_y}, {base_w}, {base_h};  {dx}:{dy}; -- {IsTarget}')


            #     #Save image for DEBUG
            #     area_img.save(f'./player_dataset/img_{dx}_{dy}.jpg')

            # break

            # Step 2 - Workout tile pixel to game pixel (game is 32x32, scaled to monitor might be bigger like 65x65...)
            tile_center_x = base_w / 2
            tile_center_y = base_h / 2

            while KeepRunning:
                # DBEUG
                # keyboard.press_and_release('1')

                # Take screenshot
                Image = ImageGrab.grab()

                # Check every tile target regions and do shit once found
                for TileInfo in DefaultSet:
                    TileSet, x, y = TileInfo
                    if target_check(Image, TileSet):
                        # OJO Grab is 37s cd
                        if time.time() - MeleeCombo[0] > 10.0:
                            # Ojou grab off cd == use
                            keyboard.press_and_release(PunchKey)
                            time.sleep(0.05)
                            keyboard.press_and_release(WebShotKey)

                            # Start ojou grab CD
                            MeleeCombo[0] = time.time()
                        else:
                            # Use other moves in rotation
                            if MeleeComboCounter > MeleeComboMaxCounter:
                                MeleeComboCounter = 1

                            fun, kwargs = MeleeCombo[MeleeComboCounter]
                            fun(**kwargs)
                            time.sleep(0.03)
                            fun(**kwargs)
                            MeleeComboCounter+=1

                        break

    
    print("Script closed")