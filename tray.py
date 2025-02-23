import sys
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

tray = None

class Tray:
    def __init__(self):
        # Create an image for the icon
        self.resolution = (64, 64)
        self.image = Image.new('RGBA', self.resolution, (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.ellipse((0, 0, 64, 64), fill="lightblue")
        self.draw.ellipse((32, 32, 48, 48), fill="blue")
        
        self.icon = Icon("icon", self.image)

        self.stopEvent = threading.Event()
        self.iconThread = threading.Thread(target=self.thread)
        self.iconThread.start()

    def thread(self):
        while not self.stopEvent.is_set():
            self.icon.run()
