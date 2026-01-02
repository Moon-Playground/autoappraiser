import asyncio
import io
import winrt.windows.media.ocr as ocr
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams

from PIL import Image
import cv2
import numpy as np


class OcrHandler:
    def init_ocr_engine(self):
        try:
            return ocr.OcrEngine.try_create_from_user_profile_languages()
        except Exception as e:
            print(f"Error initializing OCR: {e}")
            return None

    async def recognize_frame(self, ocr_engine, frame):
        if ocr_engine is None:
            return ""
        try:
            # 1. Convert to numpy array (OpenCV format)
            if isinstance(frame, imaging.SoftwareBitmap):
                # Convert SoftwareBitmap to numpy (BGRA)
                width = frame.pixel_width
                height = frame.pixel_height
                
                buf = streams.Buffer(width * height * 4)
                frame.copy_to_buffer(buf)
                
                reader = streams.DataReader.from_buffer(buf)
                pixel_bytes = bytearray(width * height * 4)
                reader.read_bytes(pixel_bytes)
                
                img = np.frombuffer(pixel_bytes, dtype=np.uint8).reshape((height, width, 4))
                # Apply green filter (BGRA -> HSV -> Mask -> BGRA)
                img = self.apply_green_filter(img, is_bgra=True)
            else:
                # Frame is already numpy (from DXCAM, usually RGB)
                img = self.apply_green_filter(frame, is_bgra=False)

            # 2. Convert back to SoftwareBitmap for Windows OCR
            # We can use the PIL path or create SoftwareBitmap directly
            pil_img = Image.fromarray(img).convert("RGB")
            
            img_byte_arr = io.BytesIO()
            pil_img.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            stream = streams.InMemoryRandomAccessStream()
            writer = streams.DataWriter(stream.get_output_stream_at(0))
            writer.write_bytes(img_bytes)
            await writer.store_async()
            
            decoder = await imaging.BitmapDecoder.create_async(stream)
            software_bitmap = await decoder.get_software_bitmap_async()
            
            # 3. Recognize
            result = await ocr_engine.recognize_async(software_bitmap)
            return result.text

        except Exception as e:
            print(f"OCR Internal Error: {e}")
            return ""

    def apply_green_filter(self, img, is_bgra=False):
        try:
            # Convert to HSV
            if is_bgra:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGRA2HSV)
            else:
                hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

            # Define green range (Adjusted for better coverage)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])

            # Mask only green areas
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Create a black background
            result = np.zeros_like(img)
            
            # Copy only the green areas
            result = cv2.bitwise_and(img, img, mask=mask)
            
            return result
        except Exception as e:
            print(f"Preprocessing Error: {e}")
            return img
