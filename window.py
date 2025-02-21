import pygame

import win32api
import win32con
import win32gui

import os

if __name__ == "__main__":
    pygame.init()

    # Setup window with no border
    screen = pygame.display.set_mode((128, 128), pygame.NOFRAME)

    # Setup variables
    done = False
    transparent = (255, 0, 255)
    red = (255, 0, 0)
    assistantName = "base"
    assistantFolder = os.path.join(os.getcwd(), "/assistants/", "/"+assistantName+"/")
    animationsFolder = os.path.join(assistantFolder, "/animations/")
    soundsFolder = os.path.join(assistantFolder, "/sounds/")
    voiceFolder = os.path.join(assistantFolder, "/voice/")
    config = os.path.join(os.getcwd(), "/config.ini")

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

    # Update loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        win32gui.EnumWindows(getWindowInformation, None)

        # Fill the screen with the color key
        screen.fill(transparent)

        # Draw square of red
        pygame.draw.rect(screen, red, pygame.Rect(32, 32, 64, 64))

        # Flip buffers around, and update window
        pygame.display.update()
