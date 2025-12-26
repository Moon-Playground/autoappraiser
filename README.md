# 🎮 AutoAppraiser

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![OS](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**AutoAppraiser** is a high-performance automation tool designed for **Fisch (Roblox)**. It utilizes advanced OCR techniques and fast screen capture to automate the appraisal process, allowing you to filter for specific fish mutations with extreme precision and speed.

---

## ✨ Key Features

-   ⚡ **Turbo Capture**: Supports both `DXCAM` (NVIDIA/AMD) and `MSS` for near-instant screen recognition.
-   👁️ **Windows Runtime OCR**: Leverages native Windows OCR for high-accuracy text detection without external dependencies like Tesseract.
-   🎯 **Overlay Region Selector**: A transparent, draggable, and resizable overlay to precisely define your capture area.
-   🧬 **Mutation Filtering**: fully customizable list of mutations to keep—stop automatically when you find that "Abyssal" or "Celestial" fish!
-   ⌨️ **Global Hotkeys**: Control the application (Toggle Overlay, Start/Stop, Force Exit) from anywhere using customizable keys.
-   🏗️ **Modular Architecture**: Clean, maintainable codebase designed for easy extension and updates.

---

## 🚀 Getting Started

### Prerequisites

-   **Windows 10/11** (Required for Windows Runtime OCR)
-   **Python 3.10 or higher**

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/autoappraiser.git
    cd autoappraiser
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

Execute the main module:
```bash
python -m autoappraiser
```

---

## 🛠️ Usage Guide

1.  **Configure Mutations**: Navigate to the "Mutations" tab and select the ones you want to keep. You can also edit the list manually.
2.  **Set Capture Region**: Press `F3` (default) to show the capture box. Drag and resize it over the appraisal text area in-game. Press `F3` again to hide and save.
3.  **Start Automating**: Equipt your fish and press `F4` to start the auto-appraisal loop. The app will automatically click the "Appraise" button and stop once a selected mutation is detected!
4.  **Test Capture**: Press `F2` to take a snapshot and see exactly what the OCR engine is reading.

---

## 🏗️ Technical Documentation

### Project Structure

```text
autoappraiser/
├── core/                # Core UI components
│   └── capture_box.py   # Draggable overlay window
├── utils/               # Logic & Utility modules
│   ├── actions.py       # Game automation / Mouse control
│   ├── camera.py        # High-speed screen capture
│   ├── config.py        # Settings & TOML management
│   ├── hotkeys.py       # Shortcut registration
│   ├── ocr_handler.py   # Windows WinRT OCR logic
│   └── mutations.py     # Filter management
└── auto_appraiser.py     # Main application & GUI (CustomTkinter)
```

### Modular Design
The project uses a **multiple inheritance pattern**. The `AutoAppraiser` class inherits from a `Utils` aggregator, which combines functionality from all utility modules. This keeps the main application lean while providing easy access to all features.

---

## 📦 Building Standalone Executable

To create a single `.exe` file for distribution:

1.  **Install PyInstaller**:
    ```bash
    pip install pyinstaller
    ```

2.  **Build**:
    ```bash
    pyinstaller autoappraiser.spec
    ```
    The output will be located in `dist/AutoAppraiser/`.

---

## 🤝 Contributing

Contributions are welcome! Whether it's fixing bugs, adding features, or improving documentation:

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Disclaimer: Use this tool responsibly. Automating gameplay may violate the terms of service of some platforms.*

