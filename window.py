import math
import pygame
from pygame._sdl2 import Window

import win32api
import win32con
import win32gui

import os

def getWindowInformation(winHwnd, extra):
    rect = win32gui.GetWindowRect(winHwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    rect = (x, y, w, h)
    name = win32gui.GetWindowText(winHwnd)
    print("Window %s:" % win32gui.GetWindowText(winHwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))

def draw_rectangle(x, y, width, height, color, rotation=0):
    """Draw a rectangle, centered at x, y.

    Arguments:
      x (int/float):
        The x coordinate of the center of the shape.
      y (int/float):
        The y coordinate of the center of the shape.
      width (int/float):
        The width of the rectangle.
      height (int/float):
        The height of the rectangle.
      color (str):
        Name of the fill color, in HTML format.
    """
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    # Convert rotation from degrees to radians.
    rot_radians = (math.pi / 180) * rotation

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)

if __name__ == "__main__":
    pygame.init()

    print("1")

    # Setup window with no border
    screen = pygame.display.set_mode((128, 128), pygame.NOFRAME)

    # Setup variables
    done = False
    transparent = (255, 0, 255)
    red = (255, 0, 0)
    assistantFolder = os.path.join(os.getcwd(), "/assistants/base/")
    animationsFolder = os.path.join(assistantFolder, "/animations/")
    soundsFolder = os.path.join(assistantFolder, "/sounds/")
    voiceFolder = os.path.join(assistantFolder, "/voice/")
    config = os.path.join(os.getcwd(), "/config.ini")
    rot = 0

    print("2")

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
    
    print("3")

    # Update loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        win32gui.EnumWindows(getWindowInformation, None)

        # Fill the screen with the color key
        screen.fill(transparent)

        # Draw square of red
        # pygame.draw.rect(screen, red, pygame.Rect(32, 32, 64, 64))

        draw_rectangle(32, 32, 64, 64, red, rot)
        rot += 1

        # Flip buffers around, and update window
        pygame.display.update()
