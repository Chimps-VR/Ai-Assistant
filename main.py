import sys


if __name__ == "__main__":
    #import intelligence
    import window
    import tray
    import pygame
    import os
    import win32gui
    import win32api
    import win32con
    from pynput.mouse import Listener

    frame = 0
    holding = False
    finalized = False
    done = False
    clock = pygame.time.Clock()
    velocity = (0,0)
    gravity = 0.4
    friction = 1.5
    offset = (0,0)
    dt = 15
    fpsDt = 1

    def onClick(x, y, button, pressed):
        global holding
        global offset
        global mouse
        global position
        if button.name == 'left':
            if pressed:
                mouseX, mouseY = win32api.GetCursorPos()
                if 0 <= mouseX-position[0] < resolution[0] and 0 <= mouseY-position[1] < resolution[1]:
                    offset = (position[0] - mouseX, position[1] - mouseY)
                    holding = True
            else:
                holding = False

    listener = Listener(on_click=onClick)
    listener.start()

    idle = ([0, 1, 2, 1], 60)
    crouch = ([3], 1)
    fall = ([4], 1)
    wobble = ([5, 6], 20)
    ouch = ([7, 8, 9, 10, 11, 12, 13, 14], 5)

    hit = False

    currAnim = idle

    assistantName = "base"
    assistantFolder = os.path.join(os.getcwd(), "assistants", assistantName)
    animationsFolder = os.path.join(assistantFolder, "animations")
    soundsFolder = os.path.join(assistantFolder, "sounds")
    voiceFolder = os.path.join(assistantFolder, "voice")
    config = os.path.join(os.getcwd(), "config.ini")

    displayInfo = {"width": win32api.GetSystemMetrics(win32con.SM_CXSCREEN), "height": win32api.GetSystemMetrics(win32con.SM_CYSCREEN)}
    print(displayInfo)

    resolution = (round(displayInfo["width"]/15), round(displayInfo["width"]/15))

    print(resolution)

    screen, hwnd = window.setupWindow(resolution)

    position = (round(displayInfo["width"]/2), round(displayInfo["height"]/2))
    lastPosition = position

    animation = window.setImages(animationsFolder)

    for frame in range(len(animation)):
        animation[frame] = window.resizeImage(animation[frame], resolution[0], resolution[1])
    animLen = len(animation)
    print(animLen)
    print(animation)

    fps = pygame.display.get_current_refresh_rate()

    trayClass = tray.Tray()

    def exitFunc():
        global done
        done = True
        trayClass.stopEvent.set()

    def hide():
        trayClass.icon.notify("Right-Click the tray then click Show to unhide the assistant.", "Assistant")
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        trayClass.icon.menu = tray.Menu(tray.MenuItem("Show", show), tray.MenuItem("Quit", exitFunc))

    def show():
        trayClass.icon.notify("Right-Click the tray then click Hide to rehide the assistant.", "Assistant")
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        trayClass.icon.menu = tray.Menu(tray.MenuItem("Hide", hide), tray.MenuItem("Quit", exitFunc))

    trayClass.icon.menu = tray.Menu(tray.MenuItem("Hide", hide), tray.MenuItem("Quit", exitFunc))

    while not done and not finalized:
        win32gui.EnumWindows(window.getWindowInformation, None)
        mouseX, mouseY = win32api.GetCursorPos()
        mouse = (mouseX, mouseY)
        position = (position[0] + velocity[0], position[1] + velocity[1])
        if holding:
            position = (mouse[0] + offset[0], mouse[1] + offset[1])
            velocity = ((position[0] - lastPosition[0])/3, (position[1] - lastPosition[1])/3)
            currAnim = wobble
        else:
            if position[1] < round(displayInfo["height"]/1.19337016575):
                velocity = (velocity[0], velocity[1] + (gravity*fpsDt))
                currAnim = fall
            else:
                velocity = (velocity[0]/friction, 0)
                position = (position[0], 905)
                hit = False
                currAnim = idle
            if position[1] < 0:
                hit = True
                position = (position[0], 0)
                velocity = (velocity[0], -velocity[1]/2)
            if position[0] < -50:
                position = (-50, position[1])
                velocity = (-50, velocity[1])
            if position[0] > displayInfo["width"]-100:
                position = (displayInfo["width"]-100, position[1])
                velocity = (displayInfo["width"]-100, velocity[1])

        if hit:
            currAnim = ouch

        done, events = window.update(frame, (round(position[0]), round(position[1])), 
                            currAnim[0][round(frame / currAnim[1]) % len(currAnim[0])], animation, screen, resolution)
        """for event in events:
            if event == 0:
                offset = (position[0] - mouse[0], position[1] - mouse[1])
                holding = True
            elif event == 1:
                holding = False"""
        frame += 1
        window.windows = []
        lastPosition = position
        dt = clock.tick(fps)
        fpsDt = dt/15

    
    velocity = (0, -10)

    while done and not finalized:
        position = (position[0] + velocity[0], position[1] + velocity[1])
        if holding:
            position = (mouse[0] + offset[0], mouse[1] + offset[1])
            velocity = ((position[0] - lastPosition[0])/3, (position[1] - lastPosition[1])/3)
            currAnim = wobble
        else:
            velocity = (velocity[0], velocity[1] + (gravity*fpsDt))
            currAnim = fall
            if position[0] < -50:
                position = (-50, position[1])
                velocity = (-50, velocity[1])
            if position[0] > displayInfo["width"]-100:
                position = (displayInfo["width"]-100, position[1])
                velocity = (displayInfo["width"]-100, velocity[1])
        if position[1] > displayInfo["height"]:
            finalized = True
        frame += 1
        lastPosition = position
        window.update(frame, (round(position[0]), round(position[1])), 
                currAnim[0][round(frame / currAnim[1]) % len(currAnim[0])], animation, screen, resolution)
        dt = clock.tick(fps)
        fpsDt = dt/15


if done:
    pygame.quit()
    trayClass.icon.stop()
    sys.exit(0)
else:
    print("WTH HAPPENED SOMETHING BROKE!!! done SHOULD BE TRUE IF WE STOPPED THE LOOP!!!")
