import os
import customtkinter
from cx_Freeze import setup, Executable

# Find customtkinter path to include its assets (json themes, etc.)
ctk_path = os.path.dirname(customtkinter.__file__)
pyarmor_src = os.path.join("dist", "pyarmor_runtime_000000")
pyarmor_dest = os.path.join("lib", "pyarmor_runtime_000000")

build_exe_options = {
    "excludes": ["unittest"],
    "packages": [
        "asyncio",
        "dxcam_cpp",
        "mss",
        "numpy",
        "keyboard",
        "tkinter",
        "tomlkit",
        "tomllib",
        "winrt",
        "winrt.windows.media.ocr",
        "winrt.windows.graphics.imaging",
        "winrt.windows.storage.streams",
        "PIL",
        "pynput",
        "customtkinter"
    ],
    "include_files": [
        (ctk_path, "customtkinter"),
        (pyarmor_src, pyarmor_dest),
        ("res", "res")
    ]
}

setup(
    name="AutoAppraise",
    version="1.0",
    description="Auto Appraise for Roblox Fisch",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "dist/auto_appraiser.py",
            base="gui",
            icon="res/icon.ico"
        )
    ],
)
