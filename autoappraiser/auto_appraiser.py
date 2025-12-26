"""
AutoAppraiser - Main Application Module

This module contains the main AutoAppraiser class which orchestrates the GUI
and application logic. Most functionality is inherited from utility modules:
- Config: Configuration management
- Camera: Screen capture functionality  
- OcrHandler: OCR text recognition
- Hotkeys: Keyboard shortcut management
- Mutations: Mutation list management
- Actions: Game automation actions
- Misc: Miscellaneous helper functions
"""

import asyncio
import customtkinter as ctk
import dxcam_cpp as dxcam
import mss
import os
import re
import threading
import time
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams

from PIL import Image
from pynput.mouse import Controller

from autoappraiser.core.capture_box import CaptureBox
from autoappraiser.utils import Utils

class AutoAppraiser(Utils):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Auto Appraiser")
        self.root.geometry("600x500")

        # Set Window Icon with robust path handling
        self.root.after(200, lambda: self._set_icon())
        
        self.capture_box = CaptureBox(
            box_color="blue",
            box_alpha=0.3,
            box_x=100,
            box_y=100,
            box_width=300,
            box_height=200,
            text="Capture Box"
        )

        self.gp_box = CaptureBox(
            box_color="green",
            box_alpha=0.3,
            box_x=639,
            box_y=517,
            box_width=85,
            box_height=50,
            text="Gamepass Button"
        )

        self.gp_confirm_box = CaptureBox(
            box_color="cyan",
            box_alpha=0.3,
            box_x=544,
            box_y=576,
            box_width=85,
            box_height=50,
            text="Confirm Button"
        )

        self.root.bind("<<ToggleBox>>", lambda e: self._toggle_box())
        self.root.bind("<<ToggleAction>>", lambda e: self._toggle_action())
        self.root.bind("<<ExitApp>>", lambda e: self._exit_app())
        self.root.bind("<<TestCapture>>", lambda e: self._test_capture())

        config = self.load_config()
        self.capture_mode = config['ocr']['capture_mode']
        self.capture_box.capture_width = config['ocr']['capture_width']
        self.capture_box.capture_height = config['ocr']['capture_height']
        self.capture_box.capture_x = config['ocr']['capture_x']
        self.capture_box.capture_y = config['ocr']['capture_y']
        self.use_gp = config['gp']['enabled']
        self.gp_box.capture_width = config['gp']['capture_width']
        self.gp_box.capture_height = config['gp']['capture_height']
        self.gp_box.capture_x = config['gp']['capture_x']
        self.gp_box.capture_y = config['gp']['capture_y']
        self.gp_confirm_box.capture_width = config['gp']['confirm_width']
        self.gp_confirm_box.capture_height = config['gp']['confirm_height']
        self.gp_confirm_box.capture_x = config['gp']['confirm_x']
        self.gp_confirm_box.capture_y = config['gp']['confirm_y']
        self.loop_interval = config['appraise']['loop_interval']
        self.fish_slot = config['appraise']['fish_slot']
        self.auto_totem = config['appraise']['auto_totem']
        self.totem_slot = config['appraise']['totem_slot']
        self.totem_interval = config['appraise']['totem_interval']
        self.last_totem = None
        self.lists = config['mutations']['lists']

        # Load Hotkeys safely
        hotkeys_conf = config.get('hotkeys', {})
        self.hk_test = hotkeys_conf.get('test_capture', 'F2')
        self.hk_box = hotkeys_conf.get('toggle_box', 'F3')
        self.hk_action = hotkeys_conf.get('toggle_action', 'F4')
        self.hk_exit = hotkeys_conf.get('exit_app', 'F5')

        if self.capture_mode == "DXCAM":
            self.camera = dxcam.create()
        elif self.capture_mode == "MSS":
            self.camera = mss.mss()
        # Initialize OCR engine
        self.ocr_engine = self.init_ocr_engine()

        self.active = threading.Event()
        self.mouse = Controller()
        self.mouse_position = None

        self.create_widgets()

    def _set_icon(self):
        try:
            icon_path = self.resource_path("res/icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                print(f"Icon not found at: {icon_path}")
        except Exception as e:
            print(f"Failed to set icon: {e}")

    def _toggle_box(self):
        if self.capture_box.state() == "withdrawn":
            self.capture_box.deiconify()
            #self.gp_box.deiconify()
            #self.gp_confirm_box.deiconify()
        else:
            self.save_config()
            self.capture_box.withdraw()
            #self.gp_box.withdraw()
            #self.gp_confirm_box.withdraw()

    def _toggle_action(self):
        if self.active.is_set():
            self.active.clear()
            self.status_label.configure(text="Status: Inactive", text_color="#ff5555")
            self.mouse_position = None
        else:
            self.active.set()
            self.status_label.configure(text="Status: Active", text_color="#2cc985")

    def _exit_app(self):
        self.save_config()
        if self.active.is_set():
            self.active.clear()
            time.sleep(0.1)
        self.root.destroy()
        # Ensure thread exit
        os._exit(0)

    def _test_capture(self):
        frame = self.capture_screen()
        if frame is not None:
            try:
                # Run async OCR in a synchronous context
                text = asyncio.run(self.read_frame(frame))
                #print(f"OCR Result: '{text}'")
                self.show_capture_dialog(frame, text)
            except Exception as e:
                #print(f"OCR Error: {e}")
                self.show_capture_dialog(frame=None, text=f"Failed to read frame: {e}")
        else:
            print("Capture returned None (check if box is within screen bounds)")
        print("-----------------------")

    def create_widgets(self):
        # Configure Grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0) # Title
        self.root.grid_rowconfigure(1, weight=1) # Main Content

        # Title Section
        self.title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.title = ctk.CTkLabel(self.title_frame, text="Auto Appraiser", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(side="left")

        self.status_label = ctk.CTkLabel(self.title_frame, text="Status: Inactive", text_color="#ff5555", font=ctk.CTkFont(size=14, weight="bold"))
        self.status_label.pack(side="right", padx=10)

        # Tabs
        self.tab_view = ctk.CTkTabview(self.root)
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.tab_mutations = self.tab_view.add("Mutations")
        self.tab_settings = self.tab_view.add("Settings")
        self.tab_hotkeys = self.tab_view.add("Hotkeys")

        # -- Mutations Tab --
        self.tab_mutations.grid_columnconfigure(0, weight=1)
        self.tab_mutations.grid_rowconfigure(0, weight=1)

        self.mutation_frame = ctk.CTkScrollableFrame(self.tab_mutations, label_text="Select Mutations to Keep")
        self.mutation_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        # Mutation Buttons
        self.mut_btn_frame = ctk.CTkFrame(self.tab_mutations, fg_color="transparent")
        self.mut_btn_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        ctk.CTkButton(self.mut_btn_frame, text="Select All", command=self.select_all_mutations, height=24).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.mut_btn_frame, text="Deselect All", command=self.deselect_all_mutations, height=24, fg_color="#555555", hover_color="#333333").pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.mut_btn_frame, text="Edit List", command=self.open_mutation_editor, height=24, fg_color="#3B8ED0", hover_color="#36719F").pack(side="left", padx=2, expand=True, fill="x")
        
        self.checkbox_vars = {}
        self.populate_mutations()

        # -- Settings Tab --
        self.tab_settings.grid_columnconfigure(0, weight=1)

        # Config Controls
        self.controls_frame = ctk.CTkFrame(self.tab_settings)
        self.controls_frame.pack(fill="x", padx=10, pady=10)

        # Capture Mode
        ctk.CTkLabel(self.controls_frame, text="Capture Mode:").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.capture_mode_var = ctk.StringVar(value=self.capture_mode)
        ctk.CTkOptionMenu(self.controls_frame, values=["DXCAM", "MSS"], variable=self.capture_mode_var).grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        # Loop Interval
        ctk.CTkLabel(self.controls_frame, text="Loop Interval (ms):").grid(row=1, column=0, padx=15, pady=15, sticky="w")
        self.loop_entry = ctk.CTkEntry(self.controls_frame, placeholder_text="2000")
        self.loop_entry.insert(0, str(self.loop_interval))
        self.loop_entry.grid(row=1, column=1, padx=10, pady=15, sticky="ew")

        # Fish Slot
        ctk.CTkLabel(self.controls_frame, text="Fish Slot (1-9):").grid(row=2, column=0, padx=15, pady=15, sticky="w")
        self.slot_entry = ctk.CTkEntry(self.controls_frame, placeholder_text="9")
        self.slot_entry.insert(0, str(self.fish_slot))
        self.slot_entry.grid(row=2, column=1, padx=10, pady=15, sticky="ew")

        # Gamepass
        ctk.CTkLabel(self.controls_frame, text="Use Gamepass").grid(row=3, column=0, padx=15, pady=15, sticky="w")
        self.use_gp_var = ctk.BooleanVar(value=self.use_gp)
        #gp_switch = ctk.CTkSwitch(self.controls_frame, variable=self.use_gp_var, text="")
        #gp_switch.configure(state="disabled")
        #gp_switch.grid(row=3, column=1, padx=10, pady=15, sticky="ew")
        ctk.CTkLabel(self.controls_frame, text="Gamepass not supported yet").grid(row=3, column=1, padx=10, pady=15, sticky="ew")

        # Save Button
        ctk.CTkButton(self.controls_frame, text="Save Settings", command=self.save_settings).grid(row=5, column=0, columnspan=2, pady=20)

        self.controls_frame.grid_columnconfigure(1, weight=1)

        # -- Hotkeys Tab --
        self.tab_hotkeys.grid_columnconfigure(0, weight=1)
        self.hk_frame = ctk.CTkFrame(self.tab_hotkeys)
        self.hk_frame.pack(fill="x", padx=10, pady=10)
        self.hk_frame.grid_columnconfigure(1, weight=1)

        # Helper to create row
        def add_hk_row(row, label, current_val):
            ctk.CTkLabel(self.hk_frame, text=label).grid(row=row, column=0, padx=15, pady=15, sticky="w")
            entry = ctk.CTkEntry(self.hk_frame)
            entry.insert(0, current_val)
            entry.grid(row=row, column=1, padx=10, pady=15, sticky="ew")
            return entry

        self.entry_test = add_hk_row(0, "Test Capture (Print):", self.hk_test)
        self.entry_box = add_hk_row(1, "Toggle Overlay:", self.hk_box)
        self.entry_action = add_hk_row(2, "Start/Stop Action:", self.hk_action)
        self.entry_exit = add_hk_row(3, "Force Exit:", self.hk_exit)

        ctk.CTkButton(self.hk_frame, text="Save & Reload Hotkeys", command=self.save_hotkeys).grid(row=4, column=0, columnspan=2, pady=20)

        # -- Totem Tab (Dynamic) --
        # Initial check
        if self.use_gp:
            self._create_totem_tab()

    def _create_totem_tab(self):
        try:
            self.totem_tab = self.tab_view.add("Totem (WIP)")
        except ValueError:
            return # Already exists

        self.totem_tab.grid_columnconfigure(0, weight=1)
        self.totem_frame = ctk.CTkFrame(self.totem_tab)
        self.totem_frame.pack(fill="x", padx=10, pady=10)
        self.totem_frame.grid_columnconfigure(1, weight=1)
        
        # Auto Totem
        ctk.CTkLabel(self.totem_frame, text="Auto Totem:").grid(row=2, column=0, padx=15, pady=15, sticky="w")
        self.auto_totem_var = ctk.BooleanVar(value=self.auto_totem)
        ctk.CTkSwitch(self.totem_frame, variable=self.auto_totem_var, text="", state="disabled").grid(row=2, column=1, padx=10, pady=15, sticky="ew")

        # Totem Slot
        ctk.CTkLabel(self.totem_frame, text="Totem Slot (1-9): ").grid(row=3, column=0, padx=15, pady=15, sticky="w")
        self.totem_slot_entry = ctk.CTkEntry(self.totem_frame, placeholder_text="8")
        self.totem_slot_entry.insert(0, str(self.totem_slot))
        self.totem_slot_entry.configure(state="disabled")
        self.totem_slot_entry.grid(row=3, column=1, padx=10, pady=15, sticky="ew")

        # Totem Interval
        ctk.CTkLabel(self.totem_frame, text="Totem Interval (Minutes): ").grid(row=4, column=0, padx=15, pady=15, sticky="w")
        self.totem_entry = ctk.CTkEntry(self.totem_frame, placeholder_text="8")
        self.totem_entry.insert(0, str(self.totem_interval))
        self.totem_entry.configure(state="disabled")
        self.totem_entry.grid(row=4, column=1, padx=10, pady=15, sticky="ew")

        # Save Button
        ctk.CTkButton(self.totem_frame, text="Save Settings", command=self.save_settings, state="disabled").grid(row=5, column=0, columnspan=2, pady=20)

    def _toggle_totem_tab(self):
        if self.use_gp_var.get():
            self._create_totem_tab()
        else:
            try:
                self.tab_view.delete("Totem (WIP)")
            except:
                pass

    async def read_frame(self, frame):
        return await self.recognize_frame(self.ocr_engine, frame)

    def appraise_worker(self):
        while True:
            self.active.wait()
            try:
                if self.use_gp: # TODO: implement gp appraise
                    #self.appraise_gp()
                    self.active.clear()
                    break
                else:
                    self.appraise_normal()

                # Give time for the GUI/Text to appear before capturing
                time.sleep(0.8) 
                
                frame = self.capture_screen()
                if frame is not None:
                    # Async call
                    result = asyncio.run(self.read_frame(frame))
                    
                    selected_lists = [desc for desc, var in self.checkbox_vars.items() if var.get()]
                    if selected_lists:
                        found_match = False
                        for desc in selected_lists:
                            if re.search(rf'{desc}', result, re.IGNORECASE):
                                # Stop the loop
                                self.active.clear()
                                self.mouse_position = None
                                
                                # Safely update GUI on main thread
                                self.root.after(0, lambda: self.status_label.configure(text="Status: Inactive", text_color="#ff5555"))
                                self.root.after(0, lambda d=desc: self.show_found_dialog(d))
                                
                                found_match = True
                                break
                        
                        if found_match:
                            continue

            except Exception as e:
                print(f"Error in worker: {e}")
                time.sleep(1)
                
            time.sleep(self.loop_interval / 1000)

    def show_capture_dialog(self, frame=None, text=None):
        top = ctk.CTkToplevel(self.root)
        top.title("Captured Image")
        # Lift window
        top.attributes("-topmost", True)

        if frame is None:
            lbl_text = ctk.CTkLabel(top, text=text, wraplength=350)
            lbl_text.pack(padx=20, pady=(0, 20))
            return

        # Convert frame to PIL Image
        if isinstance(frame, imaging.SoftwareBitmap):
            # Handle SoftwareBitmap (MSS mode)
            width = frame.pixel_width
            height = frame.pixel_height
            
            # Copy to buffer
            buf_len = width * height * 4
            buf = streams.Buffer(buf_len)
            frame.copy_to_buffer(buf)
            
            # Read bytes
            reader = streams.DataReader.from_buffer(buf)
            pixel_bytes = bytearray(buf_len)
            reader.read_bytes(pixel_bytes)
            
            # Create PIL Image (BGRA -> RGBA/RGB)
            # MSS/WinRT is usually BGRA8
            img = Image.frombytes('RGBA', (width, height), pixel_bytes, 'raw', 'BGRA')
        else:
            # Handle Numpy array (DXCAM mode)
            img = Image.fromarray(frame)

        lbl_text = ctk.CTkLabel(top, text=f"Capture Mode: {self.capture_mode}", wraplength=350)
        lbl_text.pack(padx=20, pady=(0, 0))
        
        # Create CTkImage - keeping original size
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        
        lbl_img = ctk.CTkLabel(top, text="", image=ctk_img)
        lbl_img.pack(padx=20, pady=20)
        
        lbl_text = ctk.CTkLabel(top, text=f"OCR Result:\n{text}", wraplength=350)
        lbl_text.pack(padx=20, pady=(0, 20))

    def show_found_dialog(self, text):
        top = ctk.CTkToplevel(self.root)
        top.title("Mutation Found!")
        top.geometry("300x150")
        top.attributes("-topmost", True)
        
        ctk.CTkLabel(top, text="!!! MUTATION FOUND !!!", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2cc985").pack(pady=(20, 10))
        ctk.CTkLabel(top, text=f"Mutation: {text}", font=ctk.CTkFont(size=16)).pack(pady=10)
        ctk.CTkButton(top, text="OK", command=top.destroy).pack(pady=10)

    def run(self):
        self.update_hotkeys()

        self.capture_box.geometry(f"{self.capture_box.capture_width}x{self.capture_box.capture_height}+{self.capture_box.capture_x}+{self.capture_box.capture_y}")
        self.capture_box.withdraw()

        self.gp_box.geometry(f"{self.gp_box.capture_width}x{self.gp_box.capture_height}+{self.gp_box.capture_x}+{self.gp_box.capture_y}")
        self.gp_box.withdraw()

        self.gp_confirm_box.geometry(f"{self.gp_confirm_box.capture_width}x{self.gp_confirm_box.capture_height}+{self.gp_confirm_box.capture_x}+{self.gp_confirm_box.capture_y}")
        self.gp_confirm_box.withdraw()

        threading.Thread(target=self.appraise_worker, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self._exit_app)
        self.root.mainloop()
