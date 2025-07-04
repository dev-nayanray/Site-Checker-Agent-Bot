import pyautogui
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import random
import datetime
import threading
import webbrowser
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import re

class AutomationBot:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Website Automation Bot")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Set window icon if available
        try:
            self.root.iconbitmap(self.resource_path("icon.ico"))
        except:
            pass
        
        # Create stop event
        self.stop_event = threading.Event()
        self.current_process = None
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", font=("Segoe UI", 10))
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5")
        self.style.configure("TButton", padding=6)
        self.style.configure("TNotebook", background="#f5f5f5")
        self.style.configure("TNotebook.Tab", padding=[12, 4], font=("Segoe UI", 9, "bold"))
        self.style.map("TNotebook.Tab", 
                      background=[("selected", "#5c6bc0")], 
                      foreground=[("selected", "white")])
        self.style.configure("Red.TButton", foreground="white", background="#d32f2f")
        self.style.configure("Green.TButton", foreground="white", background="#388e3c")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#333")
        self.style.configure("Section.TLabelframe.Label", font=("Segoe UI", 10, "bold"), foreground="#444")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create frames for tabs
        self.config_frame = ttk.Frame(self.notebook)
        self.log_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.config_frame, text="Configuration")
        self.notebook.add(self.log_frame, text="Execution Log")
        self.notebook.add(self.about_frame, text="About")
        
        # Header with logo
        header_frame = ttk.Frame(self.config_frame)
        header_frame.grid(row=0, column=0, columnspan=4, pady=(5, 15), sticky="ew")
        
        # Load and resize logo
        try:
            logo_img = Image.open(self.resource_path("logo.png"))
            logo_img = logo_img.resize((40, 40), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack(side="left", padx=(10, 5))
        except:
            self.logo = None
        
        header = ttk.Label(header_frame, text="Website Automation Bot", style="Header.TLabel")
        header.pack(side="left", fill="x", expand=True)
        
        # URL Section
        url_frame = ttk.LabelFrame(self.config_frame, text="Websites to Visit", style="Section.TLabelframe")
        url_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(url_frame, text="Enter URLs (one per line, max 50):").pack(anchor="w", padx=5, pady=(5, 0))
        
        # Add example URLs
        example_urls = [
            "https://www.example.com",
            "https://www.google.com",
            "https://www.github.com"
        ]
        
        self.url_entry = scrolledtext.ScrolledText(url_frame, height=8, font=("Consolas", 9), wrap="none")
        self.url_entry.pack(fill="both", expand=True, padx=5, pady=5)
        self.url_entry.insert("1.0", "\n".join(example_urls))
        
        # Time Settings Frame
        time_frame = ttk.LabelFrame(self.config_frame, text="Timing Settings", style="Section.TLabelframe")
        time_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        
        # Page Load Time
        ttk.Label(time_frame, text="Page Load Time (sec):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.load_entry = ttk.Entry(time_frame, width=8)
        self.load_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.load_entry.insert(0, "5")
        
        # Work Time per Site
        ttk.Label(time_frame, text="Work Time per Site (sec):").grid(row=0, column=2, padx=(20, 5), pady=5, sticky="w")
        self.work_entry = ttk.Entry(time_frame, width=8)
        self.work_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.work_entry.insert(0, "15")
        
        # Task Selection Frame
        tasks_frame = ttk.LabelFrame(self.config_frame, text="Automation Tasks", style="Section.TLabelframe")
        tasks_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        
        # Create a grid for checkboxes
        self.click_var = tk.BooleanVar(value=True)
        self.scroll_var = tk.BooleanVar(value=True)
        self.move_var = tk.BooleanVar(value=True)
        self.screenshot_var = tk.BooleanVar(value=False)
        self.check_var = tk.BooleanVar(value=True)
        self.read_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(tasks_frame, text="Mouse Click", variable=self.click_var).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(tasks_frame, text="Scroll Page", variable=self.scroll_var).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(tasks_frame, text="Mouse Movement", variable=self.move_var).grid(row=0, column=2, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(tasks_frame, text="Take Screenshot", variable=self.screenshot_var).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(tasks_frame, text="Check Website", variable=self.check_var).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(tasks_frame, text="Read Content", variable=self.read_var).grid(row=1, column=2, sticky="w", padx=10, pady=5)
        
        # Website Check Options Frame
        check_frame = ttk.LabelFrame(self.config_frame, text="Content Check Options", style="Section.TLabelframe")
        check_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        
        ttk.Label(check_frame, text="Keyword to check:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.keyword_entry = ttk.Entry(check_frame, width=30)
        self.keyword_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.keyword_entry.insert(0, "example")
        
        # Control Buttons Frame
        button_frame = ttk.Frame(self.config_frame)
        button_frame.grid(row=5, column=0, columnspan=4, pady=(15, 10))
        
        self.start_btn = ttk.Button(button_frame, text="▶ Start Automation", 
                                   style="Green.TButton", command=self.start_automation)
        self.start_btn.pack(side="left", padx=10, ipadx=10)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹ Stop", 
                                  style="Red.TButton", command=self.stop_automation, state="disabled")
        self.stop_btn.pack(side="left", padx=10, ipadx=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.config_frame, variable=self.progress_var, 
                                           length=400, mode="determinate")
        self.progress_bar.grid(row=6, column=0, columnspan=4, pady=(10, 5), padx=10, sticky="ew")
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to start")
        status_label = ttk.Label(self.config_frame, textvariable=self.status_var, 
                               font=("Segoe UI", 9), foreground="#333")
        status_label.grid(row=7, column=0, columnspan=4, pady=(0, 10))
        
        # Log Frame
        log_header = ttk.Frame(self.log_frame)
        log_header.pack(fill="x", padx=10, pady=(10, 5))
        
        ttk.Label(log_header, text="Execution Log", style="Header.TLabel").pack(side="left")
        
        self.clear_log_btn = ttk.Button(log_header, text="Clear Log", command=self.clear_log)
        self.clear_log_btn.pack(side="right")
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap="word", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_text.config(state="disabled")
        
        # About Frame
        about_container = ttk.Frame(self.about_frame)
        about_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        about_content = """
        Website Automation Bot v2.0

        This professional automation tool simulates human-like interactions with websites for testing, monitoring, or data collection purposes.

        Key Features:
        • Multi-tab website navigation
        • Realistic mouse movements and clicks
        • Automated scrolling and content reading
        • Keyword-based content verification
        • Screenshot capture functionality
        • Detailed execution logging
        • Progress tracking and real-time status updates

        Usage Guidelines:
        1. Enter target URLs (one per line)
        2. Configure timing parameters
        3. Select desired automation tasks
        4. Start the automation process
        5. Monitor progress in real-time
        6. Stop anytime with the stop button

        Technical Specifications:
        • Cross-platform compatibility
        • Chrome browser integration
        • Multi-threaded execution
        • Lightweight and efficient
        • Customizable delay settings

        Developed by: Nayan Ray
        Release Date: July 2023
        License: MIT Open Source
        """
        
        about_text = scrolledtext.ScrolledText(about_container, wrap="word", font=("Segoe UI", 10), height=25)
        about_text.pack(fill="both", expand=True)
        about_text.insert("1.0", about_content)
        about_text.config(state="disabled")
        
        # Footer
        footer = ttk.Frame(root)
        footer.pack(fill="x", pady=(0, 5))
        
        ttk.Label(footer, text="🔧 Developed by Nayan Ray | 🚀 Professional Automation Tool v2.0", 
                 font=("Segoe UI", 9), foreground="#666").pack(pady=5)
        
        # Configure grid weights
        self.config_frame.columnconfigure(0, weight=1)
        self.config_frame.columnconfigure(1, weight=1)
        self.config_frame.columnconfigure(2, weight=1)
        self.config_frame.columnconfigure(3, weight=1)
        
        # Set focus to URL entry
        self.url_entry.focus_set()
    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    
    def clear_log(self):
        """Clear the log window"""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.config(state="disabled")
    
    def log_message(self, message):
        """Add message to log window with timestamp"""
        self.log_text.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Color coding for different message types
        if message.startswith("✅"):
            self.log_text.tag_config("success", foreground="green")
            self.log_text.insert("end", f"[{timestamp}] ", "normal")
            self.log_text.insert("end", message + "\n", "success")
        elif message.startswith("❌") or message.startswith("⚠️"):
            self.log_text.tag_config("error", foreground="red")
            self.log_text.insert("end", f"[{timestamp}] ", "normal")
            self.log_text.insert("end", message + "\n", "error")
        elif message.startswith("🛑"):
            self.log_text.tag_config("stop", foreground="orange")
            self.log_text.insert("end", f"[{timestamp}] ", "normal")
            self.log_text.insert("end", message + "\n", "stop")
        else:
            self.log_text.insert("end", f"[{timestamp}] {message}\n")
        
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update()
    
    def human_delay(self, base=0.5, variation=0.3):
        """Random delay to simulate human behavior"""
        delay = random.uniform(base - variation, base + variation)
        self.wait_with_stop(delay)
    
    def wait_with_stop(self, seconds):
        """Wait for specified time, but check for stop event periodically"""
        start = time.time()
        while time.time() - start < seconds:
            if self.stop_event.is_set():
                return True  # Stop was requested
            time.sleep(0.1)
        return False  # Completed without stop
    
    def get_chrome_path(self):
        """Find Chrome installation path"""
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
    
    def check_website_content(self, url, keyword):
        """Check website content for a specific keyword"""
        try:
            self.log_message(f"Checking website content for keyword: {keyword}")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            
            if keyword.lower() in text:
                self.log_message(f"✅ Keyword '{keyword}' found on {url}")
                return True
            else:
                self.log_message(f"❌ Keyword '{keyword}' not found on {url}")
                return False
        except Exception as e:
            self.log_message(f"⚠️ Error checking website content: {str(e)}")
            return False
    
    def start_automation(self):
        """Start the automation process in a separate thread"""
        # Disable start button and enable stop button
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.stop_event.clear()
        
        # Clear log
        self.clear_log()
        
        # Start automation in a new thread
        automation_thread = threading.Thread(target=self.run_automation)
        automation_thread.daemon = True
        automation_thread.start()
    
    def run_automation(self):
        """Main automation function"""
        try:
            # Get input values
            urls_text = self.url_entry.get("1.0", tk.END).strip()
            load_time_text = self.load_entry.get().strip()
            work_time_text = self.work_entry.get().strip()
            keyword = self.keyword_entry.get().strip()
            
            # Parse URLs
            domains = [url.strip() for url in urls_text.split("\n") if url.startswith("http")]
            if not domains:
                self.log_message("❌ Error: Please enter at least 1 valid URL.")
                return
            elif len(domains) > 50:
                self.log_message("❌ Error: Maximum 50 URLs allowed.")
                return
            
            try:
                load_delay = int(load_time_text)
                work_time = int(work_time_text)
            except ValueError:
                self.log_message("❌ Error: Load and work times must be valid integers.")
                return
            
            # Get Chrome path
            try:
                chrome_path = self.get_chrome_path()
            except FileNotFoundError as e:
                self.log_message(f"❌ {str(e)}")
                return
            
            # Start automation
            total = len(domains)
            self.log_message(f"🚀 Starting automation for {total} websites")
            
            for index, site in enumerate(domains, start=1):
                if self.stop_event.is_set():
                    self.log_message("🛑 Automation stopped by user")
                    break
                
                # Update progress
                progress = (index / total) * 100
                self.progress_var.set(progress)
                self.update_status(f"Processing site {index}/{total}: {site}")
                
                self.log_message(f"\n🌐 Opening site {index}/{total}: {site}")
                
                try:
                    # Open Chrome in incognito mode
                    self.current_process = subprocess.Popen([chrome_path, "--incognito", site])
                except Exception as e:
                    self.log_message(f"❌ Chrome error: {str(e)}")
                    continue
                
                # Wait for page to load
                self.log_message(f"⏳ Waiting {load_delay} seconds for page to load...")
                if self.wait_with_stop(load_delay):
                    self.log_message("🛑 Stopped during page load")
                    self.current_process.terminate()
                    break
                
                # Perform website check
                if self.check_var.get() and keyword:
                    self.check_website_content(site, keyword)
                
                # Read content if enabled
                if self.read_var.get():
                    self.log_message("📖 Reading page content...")
                    self.human_delay(2.0, 0.5)
                
                # Start interaction
                self.log_message("🔄 Starting interactions...")
                start_time = time.time()
                screenshot_taken = False
                
                while (time.time() - start_time) < work_time and not self.stop_event.is_set():
                    # Randomly perform actions
                    actions = []
                    if self.click_var.get() and random.random() > 0.3:
                        actions.append("click")
                    if self.scroll_var.get() and random.random() > 0.4:
                        actions.append("scroll")
                    if self.move_var.get() and random.random() > 0.2:
                        actions.append("move")
                    if self.screenshot_var.get() and not screenshot_taken and random.random() > 0.8:
                        actions.append("screenshot")
                    
                    # Shuffle actions to randomize order
                    random.shuffle(actions)
                    
                    # Execute actions
                    for action in actions:
                        if self.stop_event.is_set():
                            break
                            
                        if action == "click":
                            x = random.randint(1000, 1000)
                            y = random.randint(600, 700)
                            self.log_message(f"🖱️ Clicking at position ({x}, {y})")
                            pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))
                            pyautogui.click()
                            self.human_delay(0.6)
                            
                        elif action == "scroll":
                            direction = random.choice([-300, -500, 300, 500])
                            self.log_message(f"📜 Scrolling {'down' if direction < 0 else 'up'} by {abs(direction)}px")
                            pyautogui.scroll(direction)
                            self.human_delay(1.2)
                            
                        elif action == "move":
                            x = random.randint(200, 1000)
                            y = random.randint(200, 700)
                            self.log_message(f"↗️ Moving mouse to ({x}, {y})")
                            pyautogui.moveTo(x, y, duration=random.uniform(0.8, 1.2))
                            self.human_delay(0.3)
                            
                        elif action == "screenshot":
                            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"screenshot_{index}_{now}.png"
                            self.log_message(f"📸 Taking screenshot: {filename}")
                            pyautogui.screenshot(filename)
                            screenshot_taken = True
                            self.human_delay(1.0)
                    
                    # Small delay between action sets
                    self.human_delay(1.0, 0.5)
                
                self.log_message(f"✅ Completed tasks for site {index}")
                
                # Close Chrome window
                self.current_process.terminate()
                self.log_message("🔒 Closed Chrome window")
                
                # Short pause between sites
                if index < total and not self.stop_event.is_set():
                    self.log_message("⏳ Preparing next website...")
                    if self.wait_with_stop(2):
                        break
            
            if not self.stop_event.is_set():
                self.log_message("\n🎉 All tasks completed successfully!")
                self.update_status("All tasks completed")
                self.progress_var.set(100)
        
        except Exception as e:
            self.log_message(f"❌ Unexpected error: {str(e)}")
        finally:
            # Re-enable start button and disable stop button
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.current_process = None
    
    def stop_automation(self):
        """Stop the automation process"""
        self.log_message("🛑 Stop requested...")
        self.stop_event.set()
        self.update_status("Stopping...")
        
        # Terminate Chrome process if running
        if self.current_process:
            try:
                self.current_process.terminate()
                self.log_message("🔒 Chrome process terminated")
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationBot(root)
    root.mainloop()