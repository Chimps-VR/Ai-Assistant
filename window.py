i
mport pygame
import win32api
import win32con
import win32gui

pygame.init()

# Setup window with no border
screen = pygame.display.set_mode((128, 128), pygame.NOFRAME)

# Setup variables
done = False
transparent = (255, 0, 255)
red = (255, 0, 0)

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

# Update loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Fill the screen with the color key
    screen.fill(transparent)

    # Draw square of red
    pygame.draw.rect(screen, red, pygame.Rect(32, 32, 64, 64))

    # Flip buffers around, and update window
    pygame.display.update()
