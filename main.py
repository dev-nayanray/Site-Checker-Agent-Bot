import pyautogui
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import random
import datetime

# Function to get Chrome path
def get_chrome_path():
    if sys.platform == 'win32':
        paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        for path in paths:
            if os.path.exists(path):
                return path
        raise FileNotFoundError("Google Chrome not found.")
    elif sys.platform == 'darwin':
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    else:
        return "/usr/bin/google-chrome"

# Human-style random delay
def human_delay(base=0.5, variation=0.3):
    time.sleep(random.uniform(base - variation, base + variation))

# Main automation function
def start_automation():
    urls_text = url_entry.get("1.0", tk.END).strip()
    load_time_text = load_entry.get().strip()
    work_time_text = work_entry.get().strip()

    domains = [url.strip() for url in urls_text.split("\n") if url.startswith("http")]
    if len(domains) < 1:
        messagebox.showerror("Error", "Please enter at least 1 valid URL.")
        return
    elif len(domains) > 50:
        messagebox.showerror("Error", "Maximum 50 URLs allowed.")
        return

    try:
        load_delay = int(load_time_text)
        work_time = int(work_time_text)
    except ValueError:
        messagebox.showerror("Error", "Load and work times must be valid integers.")
        return

    chrome_path = get_chrome_path()

    for index, site in enumerate(domains, start=1):
        print(f"\nOpening site {index}: {site}")

        try:
            current_process = subprocess.Popen([chrome_path, "--incognito", site])
        except Exception as e:
            messagebox.showerror("Error", f"Chrome error: {e}")
            return

        print(f"Waiting {load_delay} seconds for page to load...")
        time.sleep(load_delay)

        print("Starting interaction...")
        start_time = time.time()

        while (time.time() - start_time) < work_time:
            if click_var.get():
                for _ in range(2):
                    x = random.randint(200, 800)
                    y = random.randint(200, 700)
                    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))
                    pyautogui.click()
                    human_delay(0.6)

            if scroll_var.get():
                direction = random.choice([-500, 500])
                pyautogui.scroll(direction)
                human_delay(1)

            if move_var.get():
                x = random.randint(200, 1000)
                y = random.randint(200, 700)
                pyautogui.moveTo(x, y, duration=random.uniform(0.8, 1.2))
                human_delay(0.3)

            if screenshot_var.get():
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{index}_{now}.png"
                pyautogui.screenshot(filename)
                print(f"Screenshot saved: {filename}")
                screenshot_var.set(False)

        print("Task completed.")
        current_process.terminate()
        print("Closed Chrome window.")

    print("✅ All tasks completed.")

# GUI Setup
root = tk.Tk()
root.title("🧠 Website Automation Bot by Nayan Ray")
root.geometry("640x640")
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 10), background="#eef1f7")
style.configure("TCheckbutton", font=("Segoe UI", 10), background="#eef1f7")

root.configure(bg="#eef1f7")

ttk.Label(root, text="Website Automation Bot by Nayan Ray", font=("Segoe UI", 14, "bold")).pack(pady=10)

frame = ttk.Frame(root)
frame.pack(padx=20, pady=10, fill="both")

ttk.Label(frame, text="Enter URLs (1 to 50, one per line):").pack(anchor="w")
url_entry = tk.Text(frame, height=10, font=("Courier", 10))
url_entry.pack(fill="x", pady=5)

ttk.Label(frame, text="Page Load Time (sec):").pack(anchor="w", pady=(10, 0))
load_entry = ttk.Entry(frame, width=10)
load_entry.pack()
load_entry.insert(0, "5")

ttk.Label(frame, text="Work Time per Site (sec):").pack(anchor="w", pady=(10, 0))
work_entry = ttk.Entry(frame, width=10)
work_entry.pack()
work_entry.insert(0, "10")

ttk.Label(frame, text="Select Tasks:").pack(anchor="w", pady=(10, 0))
click_var = tk.BooleanVar(value=True)
scroll_var = tk.BooleanVar(value=True)
move_var = tk.BooleanVar(value=True)
screenshot_var = tk.BooleanVar(value=False)

ttk.Checkbutton(frame, text="Mouse Click", variable=click_var).pack(anchor="w")
ttk.Checkbutton(frame, text="Scroll", variable=scroll_var).pack(anchor="w")
ttk.Checkbutton(frame, text="Random Mouse Move", variable=move_var).pack(anchor="w")
ttk.Checkbutton(frame, text="Take Screenshot (1x)", variable=screenshot_var).pack(anchor="w")

ttk.Button(root, text="🚀 Start Automation", command=start_automation).pack(pady=20)

ttk.Label(root, text="🔧 Developed by Nayan Ray", font=("Segoe UI", 9)).pack(pady=5)

root.mainloop()
