import time
import keyboard as kb
from pynput.mouse import Button

class Actions:
    def do_totem(self, anchor_pos):
        if self.last_totem is None or (self.last_totem and (time.time() - self.last_totem > self.totem_interval * 60)):
            # move mouse up slightly
            self.smooth_move((anchor_pos[0], anchor_pos[1] - 200))
            time.sleep(0.5)
            self.smooth_move((anchor_pos[0] - 200, anchor_pos[1] - 200))
            time.sleep(0.3)
            # Wiggle cursor to force game game update
            self.mouse.move(2, 2)
            time.sleep(0.05)
            self.mouse.move(-2, -2)
            time.sleep(0.3)
            kb.press_and_release(str(self.totem_slot)) # Ensure string for keyboard
            time.sleep(0.3)
            self.mouse.click(Button.left)
            self.last_totem = time.time()
            time.sleep(1)
            self.smooth_move(anchor_pos)
            time.sleep(1)

    def appraise_normal(self):
        if self.mouse_position is None:
            self.mouse_position = self.mouse.position

        anchor_pos = self.mouse_position
        kb.press_and_release(str(self.fish_slot)) # Ensure string for keyboard
        time.sleep(0.5)
        self.smooth_move(anchor_pos, duration=0.1)
        self.mouse.click(Button.left)
        time.sleep(0.2)
        self.smooth_move(anchor_pos, duration=0.1)
        self.mouse.click(Button.left)
        time.sleep(self.loop_interval / 1000)
        self.smooth_move(anchor_pos, duration=0.1)
        self.mouse.click(Button.left)
        time.sleep(0.2)
        self.smooth_move(anchor_pos, duration=0.1)
        self.mouse.click(Button.left)
        time.sleep(self.loop_interval / 1000)
        self.smooth_move(anchor_pos, duration=0.1)
        self.mouse.click(Button.left)
        time.sleep(0.2)
        self.smooth_move(anchor_pos, duration=0.1)
        self.mouse.click(Button.left)
        time.sleep(self.loop_interval / 1000)

    def appraise_gp(self):
        # 1. select fish
        # 2. press `
        # 3. move mouse to gp box
        # 4. click
        # 5. move mouse to gp confirm box
        # 6. click
        pass
