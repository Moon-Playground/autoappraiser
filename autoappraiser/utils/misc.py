import time
import customtkinter as ctk
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams
from PIL import Image

class Misc:
    def smooth_move(self, mouse_controller, destination, duration=0.3):
        start_x, start_y = mouse_controller.position
        end_x, end_y = destination
        steps = max(5, int(duration * 120))

        for i in range(1, steps + 1):
            t = i / steps
            x = int(start_x + (end_x - start_x) * t)
            y = int(start_y + (end_y - start_y) * t)
            mouse_controller.position = (x, y)
            time.sleep(duration / steps)
