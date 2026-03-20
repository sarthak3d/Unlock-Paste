import time
import random
import threading
from pynput import keyboard
import pyautogui

# Fail-safe to allow users to move their mouse to a corner to stop PyAutoGUI
pyautogui.FAILSAFE = True

# Threading event to signal the typing loop to stop
stop_typing_event = threading.Event()
is_typing = False

def get_human_delay(char):
    """Calculate a human-like delay based on the character being typed."""
    if char == ' ':
        return random.uniform(0.12, 0.25)
    elif char in ['.', ',', '!', '?', '\n']:
        return random.uniform(0.25, 0.45)
    else:
        return random.uniform(0.04, 0.12)

def type_string(text, status_callback=None, completion_callback=None, progress_callback=None):
    """
    The core typing loop that writes out the characters.
    status_callback(str): Optional function to call with progress updates.
    completion_callback(int): Optional function to call when finished.
    progress_callback(int): Optional function to call with the current character index.
    """
    global is_typing
    is_typing = True
    stop_typing_event.clear()
    
    # Wait for the user to physically release any keys or move to the target window
    time.sleep(1.5)
    
    total_chars = len(text)
    
    for i, char in enumerate(text):
        if stop_typing_event.is_set():
            if status_callback:
                status_callback("Emergency abort triggered. Stopped typing.")
            break
            
        try:
            pyautogui.write(char)
            if progress_callback:
                progress_callback(i + 1)
        except Exception as e:
            pass 
            # ignore stray typings on locked os layers
            
        # Update progress occasionally
        if status_callback and i % 50 == 0 and i > 0:
            status_callback(f"Typing: {i}/{total_chars} characters...")
            
        # Simulate human resting delay
        time.sleep(get_human_delay(char))
        
    is_typing = False
    
    if completion_callback:
        completion_callback(total_chars if not stop_typing_event.is_set() else i)

# We still retain the hotkey ability for background stopping.
def on_abort_hotkey():
    stop_typing_event.set()

def start_abort_listener():
    """Starts a daemon listener for the Escape key in the background."""
    def listener_thread():
        with keyboard.GlobalHotKeys({'<esc>': on_abort_hotkey}) as h:
            h.join()
            
    t = threading.Thread(target=listener_thread, daemon=True)
    t.start()
