import os
import sys
import tomlkit
import tomllib

class Config:
    DEFAULT_CONFIG = {
        'appraise': {
            'loop_interval': 2000,
            'auto_totem': False,
            'fish_slot': 9,
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
            "Abyssal": "#0c0fd4",
            "Albino": "#fcfeff",
            "Amber": "#ff7433",
            "Big": "#8bff89",
            "Boreal": "#c8aa90",
            "Coral": "#de9bff",
            "Crimson": "#c82f2f",
            "Darkened": "#bbc5c8",
            "Electric": "#fff563",
            "Fossilized": "#d0b5ff",
            "Frozen": "#83ffe6",
            "Giant": "#8bff89",
            "Glossy": "#92e2ff",
            "Greedy": "#ffc226",
            "Hexed": "#c80000",
            "Lunar": "#bda9ff",
            "Midas": "#ff9a47",
            "Mosaic": "#fbc1ff",
            "Mourned": "#0a1427",
            "Mythical": "#ff5294",
            "Negative": "#7567e2",
            "Poisoned": "#8e65c8",
            "Scorched": "#c85530",
            "Serene": "#00ffe1",
            "Shiny": "#fff0bc",
            "Shrouded": "#a1c89e",
            "Silver": "#ceeeff",
            "Sparkling": "#fff0bc",
            "Spirit": "#846dc8",
            "Translucent": "#87ffbf",
            "Vined": "#78ce7a"
        },
        'ocr': {
            'capture_mode': 'DXCAM',
            'capture_width': 326,
            'capture_height': 98,
            'capture_x': 639,
            'capture_y': 517
        }
    }

    def save_settings(self, filepath="config.toml"):
        try:
            self.loop_interval = int(self.loop_entry.get())

            self.use_gp = self.use_gp_var.get()
            
            self.auto_totem = self.auto_totem_var.get()
            self.fish_slot = int(self.slot_entry.get())
            self.totem_slot = int(self.totem_slot_entry.get())
            self.totem_interval = int(self.totem_entry.get())
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
                'auto_totem': self.auto_totem,
                'fish_slot': self.fish_slot,
                'totem_slot': self.totem_slot,
                'totem_interval': self.totem_interval
            },
            'mutations': self.lists,
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
        # map for lookups from DEFAULT_CONFIG
        color_map = self.DEFAULT_CONFIG['mutations']

        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                cfg = tomllib.load(f)
                
                # Upgrade lists to dictionaries if they are strings
                if 'mutations' in cfg:
                    raw_mutations = cfg['mutations']
                    # Handle old format (mutations = { lists = [...] })
                    if isinstance(raw_mutations, dict) and 'lists' in raw_mutations:
                        raw_mutations = raw_mutations['lists']
                    
                    # Convert list format to flat dict if necessary
                    if isinstance(raw_mutations, list):
                        new_mutations = {}
                        for item in raw_mutations:
                            if isinstance(item, str):
                                new_mutations[item] = color_map.get(item, "#FFFFFF")
                            elif isinstance(item, dict):
                                name = list(item.keys())[0]
                                color = item[name]
                                if (color is False or color == "#FFFFFF") and name in color_map:
                                    color = color_map[name]
                                new_mutations[name] = color
                        cfg['mutations'] = new_mutations
                    elif isinstance(raw_mutations, dict):
                        # Just refresh colors if they are default
                        for name, color in raw_mutations.items():
                            if (color is False or color == "#FFFFFF") and name in color_map:
                                raw_mutations[name] = color_map[name]

                return cfg
        else:
            # Create config file if not exists
            try:
                with open(filepath, "w") as f:
                    tomlkit.dump(self.DEFAULT_CONFIG, f)
            except:
                pass 
            return self.DEFAULT_CONFIG
