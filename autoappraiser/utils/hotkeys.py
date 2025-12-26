import keyboard as kb

class Hotkeys:
    def save_hotkeys(self):
        self.hk_test = self.entry_test.get()
        self.hk_box = self.entry_box.get()
        self.hk_action = self.entry_action.get()
        self.hk_exit = self.entry_exit.get()
        self.save_config()
        self.update_hotkeys()

    def update_hotkeys(self):
        if hasattr(self, 'active_hotkeys'):
            for hk in self.active_hotkeys:
                try:
                    kb.remove_hotkey(hk)
                except:
                    pass
        
        self.active_hotkeys = []
        
        def reg(hk, event_name):
            if hk:
                try:
                    kb.add_hotkey(hk, lambda: self.root.event_generate(event_name))
                    self.active_hotkeys.append(hk)
                except Exception as e:
                    print(f"Failed to register hotkey {hk}: {e}")

        reg(self.hk_test, "<<TestCapture>>")
        reg(self.hk_box, "<<ToggleBox>>")
        reg(self.hk_action, "<<ToggleAction>>")
        reg(self.hk_exit, "<<ExitApp>>")
