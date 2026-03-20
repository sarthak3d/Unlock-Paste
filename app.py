import threading
import pyperclip
import customtkinter as ctk
from tkinter import filedialog
from human_typer import type_string, stop_typing_event, start_abort_listener

# Configure generic appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Cyberpunk Palette
CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
RED = "#FF0033"
BG_DARK = "#0d0d0d"
ACCENT_GRAY = "#1a1a1a"

class UnlockPasteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Unlock Paste")
        self.geometry("650x750")
        self.minsize(550, 650)
        self.configure(fg_color=BG_DARK)
        
        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. Header
        self.header_label = ctk.CTkLabel(
            self, text="Unlock Paste",
            font=ctk.CTkFont(family="Courier New", size=32, weight="bold"),
            text_color=CYAN
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # 2. Controls Frame
        self.source_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.source_frame.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="ew")
        self.source_frame.grid_columnconfigure((0, 1), weight=1)

        self.paste_btn = ctk.CTkButton(
            self.source_frame, text="[ Paste from Clipboard ]", 
            fg_color="transparent", hover_color=ACCENT_GRAY, 
            border_width=1, border_color=MAGENTA, text_color=MAGENTA,
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold"),
            command=self.paste_from_clipboard
        )
        self.paste_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.upload_btn = ctk.CTkButton(
            self.source_frame, text="[ Upload .txt File ]", 
            fg_color="transparent", hover_color=ACCENT_GRAY, 
            border_width=1, border_color=CYAN, text_color=CYAN,
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold"),
            command=self.load_file
        )
        self.upload_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # 3. Payload Area
        self.textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=14),
            fg_color="#121212",
            text_color="#FFFFFF",
            border_color=CYAN, 
            border_width=2
        )
        self.textbox.grid(row=3, column=0, padx=40, pady=(10, 20), sticky="nsew")
        self.textbox.insert("0.0", "AWAITING PAYLOAD INJECTION...")
        self.textbox.bind("<FocusIn>", self.clear_placeholder)
        
        # Live typing highlighting tag
        self.textbox._textbox.tag_config("typed", foreground="#00FF00")

        # 4. Action Frame
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=4, column=0, padx=40, pady=(0, 10), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_btn = ctk.CTkButton(
            self.action_frame, text="START TYPING",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            fg_color=CYAN, hover_color="#008B8B", text_color="black",
            height=60,
            command=self.start_typing_thread
        )
        self.start_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.stop_btn = ctk.CTkButton(
            self.action_frame, text="EMERGENCY ABORT",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            fg_color=RED, hover_color="#8B0000", text_color="white",
            height=60,
            command=self.abort_typing
        )
        self.stop_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # 5. Countdown Display
        self.status_display = ctk.CTkLabel(
            self, text="SYS.STATUS: [ READY ]", 
            font=ctk.CTkFont(family="Courier New", size=16, weight="bold"),
            text_color="gray"
        )
        self.status_display.grid(row=5, column=0, pady=(0, 20))

        # Start background abort listener
        start_abort_listener()

    def clear_placeholder(self, event=None):
        if self.textbox.get("0.0", "end-1c") == "AWAITING PAYLOAD INJECTION...":
            self.textbox.delete("0.0", "end")

    def paste_from_clipboard(self):
        text = pyperclip.paste()
        self.clear_placeholder()
        self.textbox.delete("0.0", "end")
        if text:
            self.textbox.insert("0.0", text)
            self.status_display.configure(text=f"SYS.STATUS: [ CLIPBOARD LOADED : {len(text)} CHARS ]", text_color=CYAN)
        else:
            self.status_display.configure(text="SYS.STATUS: [ ERROR : CLIPBOARD EMPTY ]", text_color=RED)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.clear_placeholder()
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", content)
                self.status_display.configure(text=f"SYS.STATUS: [ FILE LOADED : {file_path.split('/')[-1]} ]", text_color=MAGENTA)
            except Exception as e:
                self.status_display.configure(text=f"SYS.STATUS: [ IO.ERROR : {str(e)[:20]} ]", text_color=RED)

    def ui_status_update(self, msg):
        self.after(0, lambda: self.status_display.configure(text=msg, text_color=CYAN))
        
    def ui_completion_callback(self, chars_typed):
        self.after(0, lambda: self.status_display.configure(text=f"SYS.STATUS: [ INJECTION COMPLETE : {chars_typed} CHARS ]", text_color="#00FF00"))
        self.after(0, lambda: self.start_btn.configure(state="normal", text="START TYPING"))

    def ui_progress_update(self, current_index):
        """Applies progress color and scrolls to keep current character in view."""
        def update():
            idx = f"1.0 + {current_index}c"
            self.textbox._textbox.tag_add("typed", "1.0", idx)
            self.textbox._textbox.see(idx)
        self.after(0, update)

    def start_typing_thread(self):
        text_to_type = self.textbox.get("0.0", "end-1c").strip()
        if not text_to_type or text_to_type == "AWAITING PAYLOAD INJECTION...":
            self.status_display.configure(text="SYS.STATUS: [ CANNOT INJECT : EMPTY PAYLOAD ]", text_color=RED)
            return
            
        self.start_btn.configure(state="disabled", text="TYPING...")
        
        def countdown_task():
            import time
            stop_typing_event.clear()
            self.after(0, lambda: self.textbox._textbox.tag_remove("typed", "1.0", "end"))
            for i in range(10, 0, -1):
                if stop_typing_event.is_set():
                    self.ui_status_update("SYS.STATUS: [ ABORTED DURING COUNTDOWN ]")
                    self.after(0, lambda: self.start_btn.configure(state="normal", text="START TYPING"))
                    self.after(0, lambda: self.status_display.configure(text_color=RED))
                    return
                # Formatting seconds with leading zero for aesthetic
                self.ui_status_update(f"SYS.STATUS: [ T-MINUS 00:{i:02d} ... ASSIGN TARGET WINDOW ]")
                time.sleep(1)
                
            self.ui_status_update("SYS.STATUS: [ INJECTION COMMENCED ... DO NOT DISTURB ]")
            type_string(text_to_type, self.ui_status_update, self.ui_completion_callback, self.ui_progress_update)

        thread = threading.Thread(target=countdown_task, daemon=True)
        thread.start()

    def abort_typing(self):
        stop_typing_event.set()
        self.status_display.configure(text="SYS.STATUS: [ EMERGENCY ABORT TRIGGERED ]", text_color=RED)
        self.start_btn.configure(state="normal", text="START TYPING")

if __name__ == "__main__":
    app = UnlockPasteApp()
    app.mainloop()
