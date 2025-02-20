import pygame
import win32api
import win32con
import win32gui

pygame.init()

screen = pygame.display.set_mode((128, 128), pygame.NOFRAME)

done = False
transparent = (255, 0, 255)
red = (255, 0, 0)

hwnd = pygame.display.get_wm_info()["window"]

win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
                       )

# Set the color key to the transparent color
win32gui.SetLayeredWindowAttributes(hwnd, 
                                    win32api.RGB(*transparent), 
                                    0, 
                                    win32con.LWA_COLORKEY
                                    )

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(transparent)  # Transparent background
    pygame.draw.rect(screen, red, pygame.Rect(32, 32, 64, 64))
    pygame.display.update()
