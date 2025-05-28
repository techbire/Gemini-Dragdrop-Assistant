import os
import tkinter as tk
from tkinterdnd2 import DND_TEXT, TkinterDnD
import keyboard
import google.generativeai as genai
import threading
import queue
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Global variables
dropped_text = ''
drop_window = None
result_window = None
gui_queue = queue.Queue()

# Function to query Gemini AI
def query_gemini(prompt):
    try:
        custom_prompt = f"{prompt}\n\nGive me the direct answer from the options, no explanation."
        response = model.generate_content(custom_prompt)
        return getattr(response, 'text', 'No response from Gemini')
    except Exception as e:
        return f'Error: {e}'

# GUI loop
def gui_loop():
    root = TkinterDnD.Tk()
    root.withdraw()
    root.update_idletasks()
    screen_height = root.winfo_screenheight()

    def open_drop():
        global drop_window

        if drop_window and drop_window.winfo_exists():
            return

        drop_window = tk.Toplevel()
        drop_window.geometry(f"200x200+0+{screen_height - 200}")
        drop_window.attributes("-topmost", True)
        drop_window.overrideredirect(True)
        drop_window.configure(bg="gray")
        drop_window.wm_attributes("-transparentcolor", "gray")

        label = tk.Label(
            drop_window,
            text="Drop text here...",
            bg="gray",
            fg="light gray",
            font=("Segoe UI", 14)
        )
        label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        label.drop_target_register(DND_TEXT)
        label.dnd_bind('<<Drop>>', lambda e: on_drop(e, drop_window))

    def on_drop(event, window):
        global dropped_text
        dropped_text = event.data.strip()
        window.destroy()

    def show_result():
        global result_window, dropped_text

        if not dropped_text or (result_window and result_window.winfo_exists()):
            return

        result_window = tk.Toplevel()
        result_window.geometry(f"200x200+0+{screen_height - 370}")
        result_window.attributes("-topmost", True)
        result_window.overrideredirect(True)
        result_window.configure(bg="gray")
        result_window.wm_attributes("-transparentcolor", "gray")

        text_box = tk.Text(
            result_window,
            bg="gray",
            fg="light gray",
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            borderwidth=0,
            highlightthickness=0
        )
        text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        text_box.insert(tk.END, "Thinking...\n")
        text_box.configure(state="disabled")

        def fetch_answer():
            answer = query_gemini(dropped_text)
            text_box.configure(state="normal")
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, answer)
            text_box.configure(state="disabled")

        threading.Thread(target=fetch_answer, daemon=True).start()

    def close_all():
        global drop_window, result_window
        if drop_window and drop_window.winfo_exists():
            drop_window.destroy()
        if result_window and result_window.winfo_exists():
            result_window.destroy()
            result_window = None

    def check_queue():
        try:
            action = gui_queue.get_nowait()
            if action == 'open':
                open_drop()
            elif action == 'answer':
                show_result()
            elif action == 'close':
                close_all()
        except queue.Empty:
            pass
        root.after(100, check_queue)

    check_queue()
    root.mainloop()

# Start the GUI in a separate thread
threading.Thread(target=gui_loop, daemon=True).start()

# Global hotkeys
keyboard.add_hotkey('ctrl+z', lambda: gui_queue.put('open'))
keyboard.add_hotkey('ctrl+x', lambda: gui_queue.put('answer'))
keyboard.add_hotkey('ctrl+c', lambda: gui_queue.put('close'))

print('✅ Ctrl+Z → Open drag and drop')
print('✅ Ctrl+X → Get Gemini answer')
print('✅ Ctrl+C → Close all windows')

# Keep script running to listen for hotkeys
keyboard.wait()
