<h1 align="center">
  <img src="icon.ico" width="100" />
  <br>
  Unlock Paste
  <br>
</h1>

<h4 align="center">A Pasting tool designed to intelligently bypass anti-paste mechanisms.</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#disclaimer">Disclaimer</a> •
  <a href="#license">License</a>
</p>

---

## 🚀 Overview

Many modern websites, secure sandboxes, and remote terminals block clipboard pasting to force manual data entry or restrict automation. **Unlock Paste** circumvents these restrictions by acting as a virtual human.

Rather than injecting text instantly—which trips velocity checks and client-side listeners—Unlock Paste utilizes OS-level hardware events to physically type out your payload with dynamically calculated, human-like delays. Wrapped in a sleek, native Windows interface powered by `customtkinter`, it looks and feels like a professional toolkit.

---

## ✨ Features

- 🛡️ **OS-Level Injection:** Bypasses client-side JavaScript (`preventDefault`) and server velocity tracking via native `pyautogui` keyboard hooks.
- 🧠 **Smart Rhythm Algorithm:** Delays between characters are not static. The algorithm dynamically pauses longer for spaces, commas, periods, and new lines, perfectly mimicking natural reading and hand-adjustment pauses.
- ⏱️ **Target Acquisition Countdown:** Gives you a 10-second grace period after deployment to position your cursor on the target window before the payload drops.
- 🛑 **Global Emergency Abort:** Instantly halt the typing loop by clicking the emergency button or hitting `Esc` anywhere on your system.
- 🎨 **Cyberpunk Native UI:** A beautifully crafted deep-black and neon aesthetic built directly into a lightweight standalone Python application.
- 📋 **Payload Flexibility:** Instantly ingest payloads from your active clipboard or by parsing massive `.txt` documents.

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+ (Windows, macOS, and Linux supported)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sarthak3d/Unlock-Paste.git
   cd Unlock-Paste
   ```

2. **Set up a Virtual Environment (Recommended):**
   
   **For Windows:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   
   **For macOS and Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Core dependencies include: `customtkinter`, `pyautogui`, `pynput`, `pyperclip`)*

---

## 🎮 Usage

1. **Start the Application:**
   Ensure your virtual environment is active, then run:
   ```bash
   python app_ui.py
   ```

2. **Load your Payload:**
   Configure your text using one of the two methods above the terminal area:
   - Click **`[ Paste from Clipboard ]`**
   - Click **`[ Upload .txt File ]`**

3. **Deploy:**
   Click the massive **`START TYPING`** button.

4. **Acquire Target:**
   You have exactly 10 seconds. Click inside the exact browser text field, IDE, or terminal where you want the text to go. Let go of the mouse.

5. **Abort (If necessary):**
   If you accidentally misclicked the target window, press **`Esc`** on your physical keyboard to immediately sever the active injection loop.

---

## ⚙️ How It Works

Under the hood, Unlock Paste utilizes two primary concurrent threads. The Main Thread manages the `customtkinter` event loop to keep the UI responsive, while a Daemon Thread handles the OS interrupt.

When injection starts, the string is broken down. The `get_human_delay()` function evaluates the current character (`char`):
- **Standard AlphaNumeric:** `0.04s - 0.12s` random delay
- **Spacebars (Word Breaks):** `0.12s - 0.25s` random delay
- **Punctuation (Line Breaks):** `0.25s - 0.45s` random delay

During the sleep cycles, the application periodically checks a `threading.Event()` flag tied to the `pynput` listener. If `Esc` is detected, the event fires, and the loop is cleanly broken.

---

## 🖥️ Platform Notes (macOS & Linux)

Because Unlock Paste interacts with the Operating System at a hardware level to simulate physical keyboards and access the clipboard, non-Windows users must account for their OS security policies:

### 🍎 macOS
Apple's strict security policies block programmatic keystrokes by default. You will need to explicitly grant **Accessibility Permissions** to the terminal or IDE you are running the script from:
1. Go to **System Settings > Privacy & Security > Accessibility**.
2. Enable the toggle next to your Terminal app (e.g., iTerm, Terminal, or VS Code).
3. Without this, `pyautogui` will be blocked from typing, and `pynput` will be blocked from hearing the `Esc` abort key.

### 🐧 Linux
Linux requires a couple of underlying packages to route hardware events and clipboard data:
1. **Clipboard Support:** `pyperclip` requires either `xclip` or `xsel` installed on your system (e.g., `sudo apt-get install xclip`).
2. **Display Server:** `pyautogui` and `pynput` are designed for the **X11** windowing system. If you are on a newer distribution (like Ubuntu 22.04+) running **Wayland** by default, keystroke injection might be blocked for security reasons. You may need to switch your desktop session back to Xorg/X11 on your login screen.

---

## ⚠️ Disclaimer

Unlock Paste hooks directly into OS Core libraries to simulate physical hardware presses. 

**Be incredibly careful where your cursor is during an active injection.**
Triggering an injection without placing your cursor in the designated application could result in the payload being rapidly typed into sensitive applications, command lines, or active chat windows.

**The creator assume no liability for accidental data injection, locked-out terminals, or misuse of this tool against terms of service.** Use responsibly and strictly for environments where you lack accessible copy-paste permissions.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
