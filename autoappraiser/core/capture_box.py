import tkinter as tk

class CaptureBox(tk.Toplevel):
    def __init__(
        self,
        box_color: str = "blue",
        box_alpha: float = 0.3,
        box_x: int = 100,
        box_y: int = 100,
        box_width: int = 300,
        box_height: int = 200,
        text: str = ""
    ):
        super().__init__()
        self.capture_width, self.capture_height = box_width, box_height
        self.capture_x, self.capture_y = box_x, box_y
        self.geometry(f"{self.capture_width}x{self.capture_height}+{self.capture_x}+{self.capture_y}")
        self.overrideredirect(True)
        self.configure(bg=box_color)

        self.attributes("-alpha", 0.3)
        self.attributes("-topmost", True)

        # Dragging
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        # Resize handle
        self.resize_handle = tk.Label(self, bg="darkgreen", cursor="bottom_right_corner")
        self.resize_handle.place(relx=1.0, rely=1.0, anchor="se", width=20, height=20)
        self.resize_handle.bind("<ButtonPress-1>", self.start_resize)
        self.resize_handle.bind("<B1-Motion>", self.do_resize)

        self.text_label = tk.Label(self, text=text)
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

    def start_move(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_move(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.capture_x = self.winfo_x() + dx
        self.capture_y = self.winfo_y() + dy
        self.geometry(f"{self.capture_width}x{self.capture_height}+{self.capture_x}+{self.capture_y}")

    def start_resize(self, event):
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_orig_width = self.capture_width
        self.resize_orig_height = self.capture_height

    def do_resize(self, event):
        dx = event.x_root - self.resize_start_x
        dy = event.y_root - self.resize_start_y
        self.capture_width = max(50, self.resize_orig_width + dx)
        self.capture_height = max(50, self.resize_orig_height + dy)
        self.geometry(f"{self.capture_width}x{self.capture_height}+{self.capture_x}+{self.capture_y}")
