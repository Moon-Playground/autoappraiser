# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import customtkinter
from PyInstaller.utils.hooks import collect_all, collect_data_files

# Collect customtkinter data
ctk_datas = collect_data_files('customtkinter')
ctk_path = os.path.dirname(customtkinter.__file__)

# Collect winrt dependencies
# winrt often needs explicit collection of everything
winrt_datas, winrt_binaries, winrt_hiddenimports = collect_all('winrt')

# Specific imports that might be missed
hidden_imports = [
    'winrt.windows.media.ocr',
    'winrt.windows.graphics.imaging',
    'winrt.windows.storage.streams',
    'dxcam_cpp',
    'mss',
    'PIL',
    'pynput',
    'keyboard',
    'tomllib',
    'tomlkit'
] + winrt_hiddenimports

# Define Analysis
a = Analysis(
    ['autoappraiser/__main__.py'],
    pathex=['.'],
    binaries=winrt_binaries,
    datas=[
        ('res', 'res'),
    ] + ctk_datas + winrt_datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=False,
    name='AutoAppraiser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI only - no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon='res/icon.ico',
)

# COLLECT section removed - not needed for onefile mode
