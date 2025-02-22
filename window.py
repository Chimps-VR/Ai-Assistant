import math
import pygame
from pygame._sdl2 import Window

import win32api
import win32con
import win32gui

import os

windows = []

def setImages(path):
  image_files = [f for f in os.listdir(path)]
  
  image_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

  images = [pygame.image.load(os.path.join(path, img)).convert(32) for img in image_files]

  return images

def setupWindow(resolution):
  pygame.init()

  screen = pygame.display.set_mode(resolution, pygame.NOFRAME)

  hwnd = pygame.display.get_wm_info()["window"]

  # Set the window style
  win32gui.SetWindowLong(hwnd, 
                        win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | 
                        win32con.WS_EX_LAYERED | 
                        win32con.WS_EX_NOACTIVATE | 
                        win32con.WS_EX_TOOLWINDOW |
                        win32con.WS_EX_COMPOSITED)


  # Set the color key to the transparent color
  win32gui.SetLayeredWindowAttributes(hwnd, 
                                      win32api.RGB(*(255, 0, 255)), 
                                      0, 
                                      win32con.LWA_COLORKEY
                                      )

  win32gui.SetWindowPos(
    pygame.display.get_wm_info()['window'], 
    win32con.HWND_TOPMOST, 
    0,0,0,0, 
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )
  
  return screen, hwnd

def getWindowInformation(winHwnd, extra):
    if win32gui.IsWindowVisible(winHwnd) and not win32gui.IsIconic(winHwnd):  # Only visible & not minimized
        if win32gui.GetParent(winHwnd) == 0:  # Ensure it's a top-level window (not a child window)
            name = win32gui.GetWindowText(winHwnd).strip()
            if name and name.lower() not in ["program manager", "windows input experience"]:  # Exclude system windows
                rect = win32gui.GetWindowRect(winHwnd)
                x, y, w, h = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
                state = win32gui.GetWindowPlacement(winHwnd)[1]  # Get window state (1 = normal, 3 = maximized)

                windows.append({"name": name, "rect": rect, "state": state})

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

def resizeImage(image, screen_width, screen_height):
    img_width, img_height = image.get_width(), image.get_height()
    
    # Calculate the scale ratio for width and height
    width_ratio = screen_width / img_width
    height_ratio = screen_height / img_height
    
    # Use the smaller ratio to maintain the aspect ratio
    scale_ratio = min(width_ratio, height_ratio)
    
    # New dimensions after scaling
    new_width = int(img_width * scale_ratio)
    new_height = int(img_height * scale_ratio)
    
    # Return the resized image
    return pygame.transform.scale(image, (new_width, new_height))
  
def update(frame, rect, animationIndex, animation, screen, resolution):
  done = False
  events = []
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = event.pos

      if 0 <= mouse_x < resolution[0] and 0 <= mouse_y < resolution[1]:
         events.append(0)

    if event.type == pygame.MOUSEBUTTONUP:
       events.append(1)
       

  # Fill the screen with the color key
  screen.fill((255, 0, 255))

  screen.blit(animation[animationIndex], (0,0))

  # Flip buffers around, and update window
  pygame.display.update()

  win32gui.SetWindowPos(
     pygame.display.get_wm_info()["window"], 
     win32con.HWND_TOP, rect[0], rect[1], 128, 128, 0)

  return done, events