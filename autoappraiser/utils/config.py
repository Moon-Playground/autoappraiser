import os
import sys
import tomlkit
import tomllib

class Config:
    DEFAULT_CONFIG = {
        'appraise': {
            'loop_interval': 2000,
            'fish_slot': 9,
            'auto_totem': False,
            'totem_slot': 8,
            'totem_interval': 2
        },
        'gp': {
            'enabled': False,
            'capture_width': 85,
            'capture_height': 50,
            'capture_x': 639,
            'capture_y': 517,
            'confirm_width': 85,
            'confirm_height': 50,
            'confirm_x': 544,
            'confirm_y': 576
        },
        'hotkeys': {
            'test_capture': 'F2',
            'toggle_box': 'F3',
            'toggle_action': 'F4',
            'exit_app': 'F5'
        },
        'mutations': {
            'lists': [
                "Abyssal", "Albino", "Amber", "Crimson", "Darkened", "Electric",
                "Fossilized", "Frozen", "Glossy", "Greedy", "Hexed", "Lunar",
                "Midas", "Mosaic", "Mythical", "Negative", "Poisoned", "Scorched",
                "Shiny", "Shrouded", "Silver", "Sinister", "Sparkling", "Spirit",
                "Translucent", "Vined"
            ]
        },
        'ocr': {
            'capture_mode': 'DXCAM',
            'capture_width': 326,
            'capture_height': 98,
            'capture_x': 639,
            'capture_y': 517
        }
    }

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def save_settings(self, filepath="config.toml"):
        try:
            self.loop_interval = int(self.loop_entry.get())
            self.fish_slot = int(self.slot_entry.get())
            if self.use_gp != self.use_gp_var.get():
                self._toggle_totem_tab()
            self.use_gp = self.use_gp_var.get()
            
            if self.use_gp:
                self.auto_totem = self.auto_totem_var.get()
            
            self.totem_slot = int(self.totem_slot_entry.get()) if self.use_gp else self.totem_slot
            self.totem_interval = int(self.totem_entry.get()) if self.use_gp else self.totem_interval
            if self.capture_mode != self.capture_mode_var.get():
                self.switch_camera()
            self.capture_mode = self.capture_mode_var.get()

            self.save_config(filepath)
        except ValueError:
            print("Invalid input in settings")

    def save_config(self, filepath="config.toml"):
        cfg_data = {
            'ocr': {
                'capture_mode': self.capture_mode,
                'capture_width': self.capture_box.capture_width,
                'capture_height': self.capture_box.capture_height,
                'capture_x': self.capture_box.capture_x,
                'capture_y': self.capture_box.capture_y
            },
            'gp': {
                'enabled': self.use_gp,
                'capture_width': self.gp_box.capture_width,
                'capture_height': self.gp_box.capture_height,
                'capture_x': self.gp_box.capture_x,
                'capture_y': self.gp_box.capture_y,
                'confirm_width': self.gp_confirm_box.capture_width,
                'confirm_height': self.gp_confirm_box.capture_height,
                'confirm_x': self.gp_confirm_box.capture_x,
                'confirm_y': self.gp_confirm_box.capture_y
            },
            'appraise': {
                'loop_interval': self.loop_interval,
                'fish_slot': self.fish_slot,
                'auto_totem': self.auto_totem,
                'totem_slot': self.totem_slot,
                'totem_interval': self.totem_interval
            },
            'mutations': {
                'lists': self.lists
            },
            'hotkeys': {
                'test_capture': self.hk_test,
                'toggle_box': self.hk_box,
                'toggle_action': self.hk_action,
                'exit_app': self.hk_exit
            }
        }
        with open(filepath, "w") as f:
            tomlkit.dump(cfg_data, f)

    def load_config(self, filepath="config.toml"):
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                return tomllib.load(f)
        else:
            # Create config file if not exists
            try:
                with open(filepath, "w") as f:
                    tomlkit.dump(self.DEFAULT_CONFIG, f)
            except:
                pass 
            return self.DEFAULT_CONFIG
