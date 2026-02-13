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
            # Get target hex from selected mutation
            target_hex = None
            if hasattr(self, 'mutation_var') and hasattr(self, 'lists'):
                selected_name = self.mutation_var.get()
                if selected_name and selected_name in self.lists:
                    target_hex = self.lists[selected_name]

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
                # Apply color filter
                img = self.apply_color_filter(img, target_hex, is_bgra=True)
            else:
                # Frame is already numpy (from DXCAM, usually RGB)
                img = self.apply_color_filter(frame, target_hex, is_bgra=False)

            # 2. Convert back to SoftwareBitmap for Windows OCR
            # If image is BGRA or RGB, convert to RGB for PIL
            if img.shape[2] == 4: # BGRA
                pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGB))
            else: # RGB
                pil_img = Image.fromarray(img)
            
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

    def apply_color_filter(self, img, target_hex, is_bgra=False):
        # Only filter if we have a valid hex color
        if not target_hex or not isinstance(target_hex, str) or not target_hex.startswith("#"):
            return img
        try:
            # Convert hex to BGR
            hex_color = target_hex.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            bgr_pixel = np.uint8([[list(rgb[::-1])]])
            hsv_target = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)[0][0]
            
            h, s, v = hsv_target
            
            # Convert image to HSV
            if is_bgra:
                hsv_img = cv2.cvtColor(img, cv2.COLOR_BGRA2HSV)
            else:
                hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

            # --- Category-Based Range Logic ---
            # Instead of narrow tolerances, we use broad "buckets" for color families
            
            # Neutral colors (White, Gray, Black)
            if s < 40:
                lower = np.array([0, 0, max(40, v - 80)], dtype=np.uint8)
                upper = np.array([180, 50, 255], dtype=np.uint8)
            
            # Green-ish (including Big/Giant)
            elif 35 <= h <= 85:
                lower = np.array([35, 40, 40], dtype=np.uint8)
                upper = np.array([85, 255, 255], dtype=np.uint8)
                
            # Blue-ish (including Abyssal, Spirit, Frozen)
            elif 90 <= h <= 135:
                lower = np.array([90, 40, 40], dtype=np.uint8)
                upper = np.array([140, 255, 255], dtype=np.uint8)
            
            # Red-ish (including Crimson, Hexed)
            elif h < 15 or h > 165:
                # Primary red range
                lower = np.array([0, 40, 40], dtype=np.uint8)
                upper = np.array([15, 255, 255], dtype=np.uint8)
                # Second mask for wrap-around
                mask = cv2.inRange(hsv_img, lower, upper)
                lower2 = np.array([165, 40, 40], dtype=np.uint8)
                upper2 = np.array([180, 255, 255], dtype=np.uint8)
                mask2 = cv2.inRange(hsv_img, lower2, upper2)
                mask = cv2.bitwise_or(mask, mask2)
                return cv2.bitwise_and(img, img, mask=mask)
                
            # Yellow/Orange/Amber
            elif 15 <= h <= 35:
                lower = np.array([15, 40, 40], dtype=np.uint8)
                upper = np.array([40, 255, 255], dtype=np.uint8)
                
            # Purple/Pink/Magenta
            elif 135 < h <= 165:
                lower = np.array([135, 40, 40], dtype=np.uint8)
                upper = np.array([170, 255, 255], dtype=np.uint8)
            
            else:
                # Catch-all fallback for undefined hues
                lower = np.array([max(0, int(h) - 20), 40, 40], dtype=np.uint8)
                upper = np.array([min(180, int(h) + 20), 255, 255], dtype=np.uint8)
            
            mask = cv2.inRange(hsv_img, lower, upper)
            # Apply mask to black out everything except target color group
            result = cv2.bitwise_and(img, img, mask=mask)
            return result
        except Exception as e:
            print(f"Preprocessing Error: {e}")
            return img
