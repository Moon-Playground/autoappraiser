# AutoAppraiser Project Structure

## Overview
The AutoAppraiser project has been refactored into a modular, maintainable structure that is compatible with PyInstaller for building standalone executables.

## Directory Structure

```
autoappraiser_src/
├── autoappraiser/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── auto_appraiser.py        # Main application class
│   │
│   ├── core/                    # Core UI components
│   │   ├── __init__.py
│   │   └── capture_box.py       # Capture overlay window
│   │
│   └── utils/                   # Utility modules
│       ├── __init__.py          # Utils aggregator
│       ├── actions.py           # Game automation actions
│       ├── camera.py            # Screen capture
│       ├── config.py            # Configuration management
│       ├── hotkeys.py           # Keyboard shortcuts
│       ├── misc.py              # Helper functions
│       ├── mutations.py         # Mutation list management
│       └── ocr_handler.py       # OCR functionality
│
├── res/                         # Resources
│   └── icon.ico
│
├── config.toml                  # User configuration
├── autoappraiser.spec           # PyInstaller spec file
└── README.md                    # This file
```

## Module Responsibilities

### Main Application (`auto_appraiser.py`)
- GUI creation and layout
- Widget initialization
- Event binding
- Application lifecycle management
- Inherits functionality from all utility modules

### Core Modules

#### `core/capture_box.py`
- Transparent overlay window
- Drag and resize functionality
- Visual feedback for capture area

### Utility Modules

#### `utils/config.py`
- Configuration loading/saving (TOML format)
- Default configuration management
- Resource path resolution (PyInstaller compatible)
- Settings persistence

#### `utils/camera.py`
- Screen capture using DXCAM or MSS
- Camera mode switching
- Region-based capture
- Frame format conversion

#### `utils/ocr_handler.py`
- Windows Runtime OCR initialization
- Frame recognition (async)
- Image format conversion for OCR

#### `utils/hotkeys.py`
- Keyboard shortcut registration
- Hotkey management
- Event generation for shortcuts

#### `utils/mutations.py`
- Mutation list UI management
- Mutation editor dialog
- List persistence

#### `utils/actions.py`
- Game automation sequences
- Totem placement logic
- Fish appraisal automation
- Mouse movement and clicking

#### `utils/misc.py`
- Smooth mouse movement
- Capture preview dialog
- Mutation selection helpers
- General utility functions

## Building with PyInstaller

### Prerequisites
```bash
pip install pyinstaller
```

### Build Command
```bash
pyinstaller autoappraiser.spec
```

### Output
The built application will be in `dist/AutoAppraiser/`

## Key Features

### PyInstaller Compatibility
- Resource path resolution using `sys._MEIPASS`
- All dependencies properly collected
- Hidden imports specified in spec file
- CustomTkinter assets bundled

### Modular Design
- Single Responsibility Principle
- Easy to test individual components
- Clear separation of concerns
- Maintainable codebase

### Multiple Inheritance Pattern
The `AutoAppraiser` class inherits from `Utils`, which in turn inherits from all utility classes:
```python
class Utils(Config, Misc, OcrHandler, Hotkeys, Mutations, Camera, Actions):
    pass

class AutoAppraiser(Utils):
    # Main application logic
```

This allows the main class to access all utility methods while keeping the code organized.

## Configuration

Configuration is stored in `config.toml` with the following sections:

- `[ocr]` - Capture mode and region settings
- `[gp]` - Gamepass settings (WIP)
- `[appraise]` - Automation timing and slots
- `[mutations]` - List of mutations to detect
- `[hotkeys]` - Keyboard shortcuts

## Development

### Adding New Features
1. Identify the appropriate utility module (or create a new one)
2. Add the functionality to that module as a class method
3. If creating a new module, add it to `utils/__init__.py`
4. The main application will automatically have access to the new methods

### Testing
Each utility module can be tested independently since they're separate classes.

## Dependencies

- customtkinter - Modern UI framework
- dxcam_cpp - Fast screen capture
- mss - Cross-platform screen capture
- keyboard - Keyboard event handling
- pynput - Mouse control
- winrt - Windows Runtime OCR
- PIL - Image processing
- tomlkit/tomllib - Configuration management
