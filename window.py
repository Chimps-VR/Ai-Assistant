import math
import pygame
from pygame._sdl2 import Window

import win32api
import win32con
import win32gui

import os

pygame.init()

# Setup window with no border
screen = pygame.display.set_mode((256, 256), pygame.NOFRAME)
window = Window.from_display_module()
window.position = (10, 30)

# Setup variables
done = False
frame = 0
winRect = (0, 0, 256, 256)
windowRects = []
transparent = (255, 0, 255)
red = (255, 0, 0)
assistant = "base"
assistantFolder = os.path.join(os.getcwd(), "/assistants/", f"/{assistant}/")
animationsFolder = os.path.join(assistantFolder, "/animations/")
soundsFolder = os.path.join(assistantFolder, "/sounds/")
voiceFolder = os.path.join(assistantFolder, "/voice/")
config = os.path.join(os.getcwd(), "/config.ini")

assistantAnimations = []

# Get window
hwnd = pygame.display.get_wm_info()["window"]

# Set the window style
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
                       )

# Set the color key to the transparent color
win32gui.SetLayeredWindowAttributes(hwnd, 
                                    win32api.RGB(*transparent), 
                                    0, 
                                    win32con.LWA_COLORKEY
                                    )

def getWindowInformation(winHwnd, none):
    if win32gui.IsWindowVisible(winHwnd):
        winRect = win32gui.GetWindowRect(winHwnd)
        name = win32gui.GetWindowText(winHwnd)
        if winRect[0] > -30000 and abs(winRect[0]) > 0 and name:
            x = winRect[0]
            y = winRect[1]
            w = winRect[2] - x
            h = winRect[3] - y
            rect = (x, y, w, h)
            windowRects.append(rect)
            print(name)
            print(rect)

def find_window_by_name(window_name, windowRects):
    for window in windowRects:
        if window[0] == window_name:
            return window
    return None

# Update loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Reset window rects and get them again
    windowRects = []
    win32gui.EnumWindows(getWindowInformation, None)

    # Fill the screen with the color key
    screen.fill(transparent)

    # Draw square of red
    pygame.draw.rect(screen, red, pygame.Rect(256/2, 256/2, 128, 128))

    # Move Window
    winRect = (window.position[0]+[0], window.position[1]+windowRects[2][1])

    # Flip buffers around, and update window position
    window.position = (winRect[0], winRect[1])
    pygame.display.update()
    frame += 1
