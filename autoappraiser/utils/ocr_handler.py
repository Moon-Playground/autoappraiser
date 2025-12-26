import asyncio
import io
import winrt.windows.media.ocr as ocr
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams
from PIL import Image


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
            if isinstance(frame, imaging.SoftwareBitmap):
                result = await ocr_engine.recognize_async(frame)
                return result.text

            # 1. Convert to PIL Image
            img = Image.fromarray(frame).convert("RGB")
            
            # 2. Save image to in-memory PNG
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            # 3. Write data to Windows RandomAccessStream
            stream = streams.InMemoryRandomAccessStream()
            writer = streams.DataWriter(stream.get_output_stream_at(0))
            writer.write_bytes(img_bytes)
            await writer.store_async()
            
            # 4. Use BitmapDecoder to interpret the image
            decoder = await imaging.BitmapDecoder.create_async(stream)
            
            # 5. Get SoftwareBitmap from decoder
            software_bitmap = await decoder.get_software_bitmap_async()
            
            # 6. Recognize
            result = await ocr_engine.recognize_async(software_bitmap)
            return result.text
            
        except Exception as e:
            print(f"OCR Internal Error: {e}")
            return ""
