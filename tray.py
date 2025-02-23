import sys
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

tray = None

class Tray:
    def __init__(self):
        # Create an image for the icon
        self.resolution = (256, 256)
        self.image = Image.new('RGBA', self.resolution, (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)

        self.iconImage = Image.open("icon.ico")

        self.image.paste(self.iconImage, (0, 0), self.iconImage) # first for color third for transparency
        
        self.icon = Icon("icon", self.image)

        self.stopEvent = threading.Event()
        self.iconThread = threading.Thread(target=self.thread)
        self.iconThread.start()

    def thread(self):
        while not self.stopEvent.is_set():
            self.icon.run()
