from .config import Config
from .misc import Misc
from .ocr_handler import OcrHandler
from .hotkeys import Hotkeys
from .mutations import Mutations
from .camera import Camera
from .actions import Actions

class Utils(Config, Misc, OcrHandler, Hotkeys, Mutations, Camera, Actions):
    pass
