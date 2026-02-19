import time
import platform
import keyboard as kb

# Platform specific imports
IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    try:
        import pydirectinput
    except ImportError:
        IS_WINDOWS = False

if not IS_WINDOWS:
    import pyautogui
    # PyAutoGUI failsafe can be annoying in some games, but good for safety
    pyautogui.FAILSAFE = False


class Actions:
    def _move_to(self, x, y):
        if IS_WINDOWS:
            pydirectinput.moveTo(int(x), int(y))
        else:
            pyautogui.moveTo(int(x), int(y))

    def _click(self):
        if IS_WINDOWS:
            pydirectinput.click()
        else:
            pyautogui.click()

    def _get_position(self):
        if IS_WINDOWS:
            return pydirectinput.position()
        else:
            return pyautogui.position()

    def do_totem(self, anchor_pos):
        if self.last_totem is None or (self.last_totem and (time.time() - self.last_totem > self.totem_interval * 60)):
            # move mouse up slightly
            self._move_to(anchor_pos[0], anchor_pos[1] - 200)
            time.sleep(0.5)
            # keyboard library usually works on Linux if root/udev is set, 
            # but we can use pyautogui as fallback if needed.
            kb.press_and_release(str(self.totem_slot)) 
            time.sleep(0.3)
            self._click()
            self.last_totem = time.time()
            time.sleep(1)
            self._move_to(anchor_pos[0], anchor_pos[1])
            time.sleep(1)
            kb.press_and_release(str(self.fish_slot))
            time.sleep(0.5)

    def appraise_normal(self):
        if self.mouse_position is None:
            self.mouse_position = self._get_position()

        anchor_pos = self.mouse_position
        self._move_to(anchor_pos[0], anchor_pos[1])
        self._click()
        time.sleep(0.2)
        self._move_to(anchor_pos[0], anchor_pos[1])
        self._click()
        time.sleep(self.loop_interval / 1000)
        self._move_to(anchor_pos[0], anchor_pos[1])
        self._click()
        time.sleep(0.2)
        self._move_to(anchor_pos[0], anchor_pos[1])
        self._click()
        time.sleep(self.loop_interval / 1000)

    def appraise_gp(self):
        # 1. select fish
        # 2. press `
        # 3. move mouse to gp box
        # 4. click
        # 5. move mouse to gp confirm box
        # 6. click
        pass
