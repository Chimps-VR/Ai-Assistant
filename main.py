if __name__ == "__main__":
    #import intelligence
    import window
    import pygame
    import os
    import win32gui
    import win32api
    from pynput.mouse import Listener

    resolution = (128, 128)
    frame = 0
    holding = False
    done = False
    clock = pygame.time.Clock()
    velocity = (3,0)
    position = (0,0)
    lastPosition = (0,0)
    gravity = 0.4
    friction = 1.5
    offset = (0,0)
    dt = 0

    def on_click(x, y, button, pressed):
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

    listener = Listener(on_click=on_click)
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

    animation = window.setImages(animationsFolder)

    for frame in range(len(animation)):
        animation[frame] = window.resizeImage(animation[frame], resolution[0], resolution[1])
    animLen = len(animation)

    screen, hwnd = window.setupWindow(resolution)

    fps = pygame.display.get_current_refresh_rate()

    while not done:
        win32gui.EnumWindows(window.getWindowInformation, None)
        mouseX, mouseY = win32api.GetCursorPos()
        mouse = (mouseX, mouseY)
        position = (position[0] + velocity[0], position[1] + velocity[1])
        if holding:
            position = (mouse[0] + offset[0], mouse[1] + offset[1])
            velocity = ((position[0] - lastPosition[0])/3, (position[1] - lastPosition[1])/3)
            currAnim = wobble
        else:
            if position[1] < 905:
                velocity = (velocity[0], velocity[1] + gravity)
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
            if position[0] > 1920-100:
                position = (1920-100, position[1])
                velocity = (1920-100, velocity[1])

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
