import platform

# Platform specific imports
IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    try:
        import dxcam_cpp as dxcam
        import winrt.windows.graphics.imaging as imaging
        import winrt.windows.storage.streams as streams
    except ImportError:
        IS_WINDOWS = False

import mss
import numpy as np
from PIL import Image

class Camera:
    def switch_camera(self):
        if IS_WINDOWS and self.capture_mode == "DXCAM":
            self.camera = dxcam.create()
        else:
            self.camera = mss.mss()

    def capture_screen(self):
        if self.camera is None:
            return None

        # Get screen dimensions from tkinter or safe default
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int(self.capture_box.capture_x)
        y = int(self.capture_box.capture_y)
        w = int(self.capture_box.capture_width)
        h = int(self.capture_box.capture_height)

        # Region calculation
        left = max(0, x)
        top = max(0, y)
        right = min(screen_width, x + w)
        bottom = min(screen_height, y + h)

        # Ensure valid region
        if right <= left or bottom <= top:
            return None

        try:
            if IS_WINDOWS and self.capture_mode == "DXCAM":
                frame = self.camera.grab(region=(left, top, right, bottom))
            else:
                sct_img = self.camera.grab({"top": top, "left": left, "width": w, "height": h})
                
                if IS_WINDOWS:
                    # Create IBuffer from bytes via DataWriter for Windows OCR
                    data_writer = streams.DataWriter()
                    data_writer.write_bytes(sct_img.raw)
                    ibuffer = data_writer.detach_buffer()

                    frame = imaging.SoftwareBitmap.create_copy_from_buffer(
                        ibuffer,
                        imaging.BitmapPixelFormat.BGRA8,
                        int(sct_img.width),
                        int(sct_img.height)
                    )
                else:
                    # On Linux, return as PIL Image or Numpy array
                    frame = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            return frame
        except Exception as e:
            print(f"Capture error: {e}")
            return None
        except Exception as e:
            print(f"Capture error: {e}")
            return None
