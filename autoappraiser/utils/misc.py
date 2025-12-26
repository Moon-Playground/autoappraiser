import time
import customtkinter as ctk
import sys
import os
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

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller/Nuitka """
        if getattr(sys, 'frozen', False):
            # If frozen (PyInstaller, Nuitka, cx_Freeze)
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller
                base_path = sys._MEIPASS
            else:
                # Nuitka, cx_Freeze
                base_path = os.path.dirname(sys.executable)
        else:
            # Development: use the directory of the package
            # This file is in autoclicker/utils, so the package root is one level up
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        full_path = os.path.join(base_path, relative_path)
        
        # Fallback to CWD if not found, for backward compatibility
        if not os.path.exists(full_path):
            cwd_path = os.path.join(os.path.abspath("."), relative_path)
            if os.path.exists(cwd_path):
                return cwd_path
                
        return full_path
