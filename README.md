# 🎮 AutoAppraiser

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![OS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**AutoAppraiser** is a high-performance automation tool designed for **Fisch (Roblox)**. It utilizes advanced OCR techniques and fast screen capture to automate the appraisal process, allowing you to filter for specific fish mutations with extreme precision and speed. Now supporting both **Windows** and **Linux**!

---

## ✨ Key Features

-   ⚡ **Turbo Capture**: Supports both `DXCAM` (Windows/NVIDIA/AMD) and `MSS` (Cross-platform) for near-instant screen recognition.
-   👁️ **Dual OCR Support**: 
    -   **Windows**: Native Windows Runtime OCR (High-accuracy, no dependencies).
    -   **Linux**: Tesseract OCR (Robust, open-source).
-   🎯 **Overlay Region Selector**: A transparent, draggable, and resizable overlay to precisely define your capture area.
-   🧬 **Mutation Filtering**: Fully customizable list of mutations to keep—stop automatically when you find that "Abyssal" or "Celestial" fish!
-   ⌨️ **Global Hotkeys**: Control the application (Toggle Overlay, Start/Stop, Force Exit) from anywhere using customizable keys.

---

## 🚀 Getting Started

### Prerequisites

-   **Python 3.10 or higher**
-   **Windows**:
    -   Native **Windows Runtime OCR** (Recommended, no extra install).
    -   **Tesseract OCR** (Optionally, as an alternative/fallback. Requires Tesseract to be installed on your system).
-   **Linux**:
    -   `tesseract-ocr` (e.g., `sudo apt install tesseract-ocr`)
    -   `Tkinter` (e.g., `sudo apt install python3-tk`)
    -   X11 Environment (Wayland support varies by distro)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Moon-Playground/fisch-autoappraiser.git
    cd fisch-autoappraiser
    ```

2.  **Install dependencies:**
    -   **Windows**:
        ```bash
        pip install ".[windows]"
        ```
    -   **Linux**:
        ```bash
        pip install ".[linux]"
        ```

### Running the App

Execute the main module:
```bash
python -m autoappraiser
```

---

## 🛠️ Usage Guide

See [USAGE.md](USAGE.md)

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
