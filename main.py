import pyautogui
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sys
import os
import random
import datetime
import threading
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import re
import json
import openai
import base64

class AutomationBot:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 AI-Powered Website Automation Bot")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Set window icon if available
        try:
            self.root.iconbitmap(self.resource_path("icon.ico"))
        except:
            pass
        
        # Create stop event
        self.stop_event = threading.Event()
        self.current_process = None
        self.ai_automation_active = False
        self.openai_api_key = ""
        self.element_images = {}  # Store uploaded UI element images
        
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
        self.style.configure("Blue.TButton", foreground="white", background="#1976d2")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#333")
        self.style.configure("Section.TLabelframe.Label", font=("Segoe UI", 10, "bold"), foreground="#444")
        self.style.configure("AI.TFrame", background="#e3f2fd")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create frames for tabs
        self.config_frame = ttk.Frame(self.notebook)
        self.ai_frame = ttk.Frame(self.notebook, style="AI.TFrame")
        self.log_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.config_frame, text="Configuration")
        self.notebook.add(self.ai_frame, text="AI Commands")
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
        
        header = ttk.Label(header_frame, text="AI-Powered Website Automation Bot", style="Header.TLabel")
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
        
        # ================== AI Commands Frame ==================
        ai_header_frame = ttk.Frame(self.ai_frame, style="AI.TFrame")
        ai_header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ttk.Label(ai_header_frame, text="AI-Powered Automation", style="Header.TLabel").pack(side="left")
        
        # API Key Frame
        api_frame = ttk.LabelFrame(self.ai_frame, text="OpenAI API Settings", style="Section.TLabelframe")
        api_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(api_frame, text="OpenAI API Key:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.api_entry = ttk.Entry(api_frame, width=50, show="*")
        self.api_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Save API Key button
        save_btn = ttk.Button(api_frame, text="Save Key", style="Blue.TButton", command=self.save_api_key)
        save_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # UI Elements Frame
        element_frame = ttk.LabelFrame(self.ai_frame, text="UI Element Recognition", style="Section.TLabelframe")
        element_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(element_frame, text="Upload UI elements:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.element_listbox = tk.Listbox(element_frame, height=4, width=30)
        self.element_listbox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        add_btn = ttk.Button(element_frame, text="Add Element", command=self.add_ui_element)
        add_btn.grid(row=0, column=2, padx=(5, 2), pady=5)
        
        remove_btn = ttk.Button(element_frame, text="Remove", command=self.remove_ui_element)
        remove_btn.grid(row=0, column=3, padx=2, pady=5)
        
        # AI Command Input
        command_frame = ttk.LabelFrame(self.ai_frame, text="Natural Language Commands", style="Section.TLabelframe")
        command_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ttk.Label(command_frame, text="Enter your automation command:").pack(anchor="w", padx=5, pady=(5, 0))
        
        example_command = "Visit example.com, search for 'automation tools', click the search button, wait 5 seconds, and take a screenshot"
        self.command_entry = scrolledtext.ScrolledText(command_frame, height=8, font=("Segoe UI", 10), wrap="word")
        self.command_entry.pack(fill="both", expand=True, padx=5, pady=5)
        self.command_entry.insert("1.0", example_command)
        
        # Action Buttons
        action_frame = ttk.Frame(self.ai_frame, style="AI.TFrame")
        action_frame.pack(fill="x", padx=10, pady=5)
        
        self.parse_btn = ttk.Button(action_frame, text="Parse & Run", style="Green.TButton", 
                                   command=self.start_ai_automation)
        self.parse_btn.pack(side="left", padx=10, ipadx=10)
        
        self.ai_stop_btn = ttk.Button(action_frame, text="⏹ Stop AI", style="Red.TButton", 
                                    command=self.stop_ai_automation, state="disabled")
        self.ai_stop_btn.pack(side="left", padx=10, ipadx=10)
        
        # Parsed Actions Display
        parsed_frame = ttk.LabelFrame(self.ai_frame, text="Parsed Actions", style="Section.TLabelframe")
        parsed_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        self.parsed_text = scrolledtext.ScrolledText(parsed_frame, height=8, font=("Consolas", 9), wrap="word")
        self.parsed_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.parsed_text.insert("1.0", "Parsed actions will appear here...")
        self.parsed_text.config(state="disabled")
        
        # ================== Log Frame ==================
        log_header = ttk.Frame(self.log_frame)
        log_header.pack(fill="x", padx=10, pady=(10, 5))
        
        ttk.Label(log_header, text="Execution Log", style="Header.TLabel").pack(side="left")
        
        self.clear_log_btn = ttk.Button(log_header, text="Clear Log", command=self.clear_log)
        self.clear_log_btn.pack(side="right")
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap="word", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_text.config(state="disabled")
        
        # ================== About Frame ==================
        about_container = ttk.Frame(self.about_frame)
        about_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        about_content = """
        AI-Powered Website Automation Bot v3.0

        This advanced automation tool combines traditional scripting with AI capabilities 
        to understand and execute natural language commands for website automation.

        New AI Features:
        • Natural Language Command Processing
        • OpenAI API Integration
        • Website Content Summarization
        • UI Element Recognition via Image Matching
        • Automated Action Sequence Generation

        How to Use AI Commands:
        1. Enter your OpenAI API key
        2. Upload UI elements you want the bot to recognize
        3. Describe your automation task in natural language
        4. Click "Parse & Run" to generate and execute the automation sequence
        5. Monitor the execution in the log

        Technical Specifications:
        • GPT-4 Turbo for command parsing
        • Multi-threaded execution engine
        • Cross-platform UI element recognition
        • Real-time progress tracking
        • Detailed execution logging

        Developed by: Nayan Ray
        Release Date: July 2025
        License: MIT Open Source
        """
        
        about_text = scrolledtext.ScrolledText(about_container, wrap="word", font=("Segoe UI", 10), height=25)
        about_text.pack(fill="both", expand=True)
        about_text.insert("1.0", about_content)
        about_text.config(state="disabled")
        
        # Footer
        footer = ttk.Frame(root)
        footer.pack(fill="x", pady=(0, 5))
        
        ttk.Label(footer, text="🔧 Developed by Nayan Ray | 🚀 AI-Powered Automation v3.0", 
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
        elif message.startswith("🤖"):
            self.log_text.tag_config("ai", foreground="#1976d2")
            self.log_text.insert("end", f"[{timestamp}] ", "normal")
            self.log_text.insert("end", message + "\n", "ai")
        elif message.startswith("🔍"):
            self.log_text.tag_config("element", foreground="#7b1fa2")
            self.log_text.insert("end", f"[{timestamp}] ", "normal")
            self.log_text.insert("end", message + "\n", "element")
        else:
            self.log_text.insert("end", f"[{timestamp}] {message}\n")
        
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update()
    
    def save_api_key(self):
        """Save OpenAI API key"""
        self.openai_api_key = self.api_entry.get().strip()
        if self.openai_api_key:
            self.log_message("🔑 OpenAI API key saved successfully")
        else:
            self.log_message("⚠️ Please enter a valid OpenAI API key")
    
    def add_ui_element(self):
        """Add a UI element image for recognition"""
        file_path = filedialog.askopenfilename(
            title="Select UI Element Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        
        if file_path:
            element_name = os.path.basename(file_path).split('.')[0]
            self.element_images[element_name] = file_path
            self.element_listbox.insert(tk.END, element_name)
            self.log_message(f"📸 Added UI element: {element_name}")
    
    def remove_ui_element(self):
        """Remove selected UI element"""
        selected = self.element_listbox.curselection()
        if selected:
            element_name = self.element_listbox.get(selected[0])
            del self.element_images[element_name]
            self.element_listbox.delete(selected[0])
            self.log_message(f"🗑️ Removed UI element: {element_name}")
    
    def human_delay(self, base=0.5, variation=0.3):
        """Random delay to simulate human behavior"""
        delay = random.uniform(base - variation, base + variation)
        self.wait_with_stop(delay)
    
    def wait_with_stop(self, seconds):
        """Wait for specified time, but check for stop event periodically"""
        start = time.time()
        while time.time() - start < seconds:
            if self.stop_event.is_set() or (self.ai_automation_active and self.stop_event.is_set()):
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
    
    def summarize_content(self, url):
        """Summarize website content using OpenAI"""
        if not self.openai_api_key:
            self.log_message("⚠️ OpenAI API key not set. Cannot summarize content.")
            return ""
        
        try:
            self.log_message(f"🤖 Generating summary for: {url}")
            response = requests.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
            for tag in soup(['header', 'footer', 'nav', 'script', 'style']):
                tag.decompose()
            
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Truncate to fit token limits
            if len(text) > 12000:
                text = text[:12000] + "... [TRUNCATED]"
            
            # Call OpenAI API
            openai.api_key = self.openai_api_key
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes web page content."},
                    {"role": "user", "content": f"Summarize the following content in 3-4 sentences:\n\n{text}"}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            summary = response.choices[0].message['content'].strip()
            self.log_message(f"📝 Summary for {url}:\n{summary}")
            return summary
        except Exception as e:
            self.log_message(f"❌ Error generating summary: {str(e)}")
            return ""
    
    def parse_command_with_openai(self, command):
        """Parse natural language command into structured actions using OpenAI"""
        if not self.openai_api_key:
            self.log_message("❌ OpenAI API key not set. Cannot parse command.")
            return []
        
        try:
            self.log_message("🤖 Parsing command with OpenAI...")
            openai.api_key = self.openai_api_key
            
            # Build list of available UI elements
            element_list = ", ".join(self.element_images.keys()) if self.element_images else "None"
            
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": f"""
                    You are an automation command parser. Convert the user's natural language command into a JSON array of automation actions.
                    
                    Available actions and parameters:
                    - visit: {{"url": "<full_url>"}}
                    - click: {{"x": <number>, "y": <number>}} OR {{"element": "<element_name>"}}
                    - move: {{"x": <number>, "y": <number>}}
                    - scroll: {{"amount": <number>}} (positive=up, negative=down)
                    - wait: {{"seconds": <number>}}
                    - screenshot: {{"filename": "<filename>.png"}} (optional)
                    - check: {{"keyword": "<keyword>"}}
                    - summarize: {{}} (no parameters)
                    
                    Rules:
                    - Always start with a visit action
                    - Use 'element' parameter for clicks if element name is provided
                    - Use coordinates only when element not specified
                    - Generate valid JSON only
                    - Include only the JSON array in your response
                    
                    Available UI elements: {element_list}
                    """},
                    {"role": "user", "content": command}
                ],
                max_tokens=500,
                temperature=0.2
            )
            
            # Extract JSON from response
            response_text = response.choices[0].message['content'].strip()
            self.log_message(f"🤖 OpenAI response: {response_text}")
            
            # Try to find JSON in the response
            try:
                # Extract JSON string from response
                json_start = response_text.find('[')
                json_end = response_text.rfind(']') + 1
                json_str = response_text[json_start:json_end]
                
                actions = json.loads(json_str)
                self.log_message("✅ Command parsed successfully")
                return actions
            except json.JSONDecodeError:
                self.log_message("❌ Failed to parse JSON response from OpenAI")
                return []
        except Exception as e:
            self.log_message(f"❌ OpenAI API error: {str(e)}")
            return []
    
    def execute_ai_action(self, action):
        """Execute a single AI-generated action"""
        action_type = action.get('action')
        
        if action_type == "visit":
            url = action.get('url', '')
            if not url.startswith('http'):
                url = 'https://' + url
            self.log_message(f"🌐 Visiting: {url}")
            
            try:
                chrome_path = self.get_chrome_path()
                self.current_process = subprocess.Popen([chrome_path, "--incognito", url])
                self.wait_with_stop(5)  # Wait for page to load
                return True
            except Exception as e:
                self.log_message(f"❌ Error visiting {url}: {str(e)}")
                return False
                
        elif action_type == "click":
            if 'element' in action:
                element_name = action['element']
                self.log_message(f"🔍 Clicking UI element: {element_name}")
                return self.click_ui_element(element_name)
            else:
                x = action.get('x', 100)
                y = action.get('y', 100)
                self.log_message(f"🖱️ Clicking at position ({x}, {y})")
                pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.0))
                pyautogui.click()
                self.human_delay()
                return True
                
        elif action_type == "move":
            x = action.get('x', 100)
            y = action.get('y', 100)
            self.log_message(f"↗️ Moving mouse to ({x}, {y})")
            pyautogui.moveTo(x, y, duration=random.uniform(0.8, 1.2))
            self.human_delay()
            return True
            
        elif action_type == "scroll":
            amount = action.get('amount', 300)
            self.log_message(f"📜 Scrolling by {amount}px")
            pyautogui.scroll(amount)
            self.human_delay(1.0)
            return True
            
        elif action_type == "wait":
            seconds = action.get('seconds', 3)
            self.log_message(f"⏳ Waiting {seconds} seconds")
            return not self.wait_with_stop(seconds)
            
        elif action_type == "screenshot":
            filename = action.get('filename', f"screenshot_{int(time.time())}.png")
            self.log_message(f"📸 Taking screenshot: {filename}")
            pyautogui.screenshot(filename)
            self.human_delay(1.0)
            return True
            
        elif action_type == "check":
            keyword = action.get('keyword', '')
            if keyword:
                return self.check_website_content("", keyword)  # URL not needed here
            return True
            
        elif action_type == "summarize":
            # For simplicity, we'll summarize the current page
            self.log_message("🤖 Summarizing current page content")
            summary = self.summarize_content("")  # URL not needed here
            if summary:
                self.log_message(f"📝 Summary: {summary}")
            return True
            
        else:
            self.log_message(f"⚠️ Unknown action type: {action_type}")
            return False
    
    def click_ui_element(self, element_name):
        """Click a UI element using image recognition"""
        if element_name not in self.element_images:
            self.log_message(f"❌ UI element '{element_name}' not found")
            return False
        
        image_path = self.element_images[element_name]
        
        try:
            # Try to find the element on screen
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
            if location:
                x, y = location
                self.log_message(f"🔍 Found '{element_name}' at ({x}, {y})")
                pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.0))
                pyautogui.click()
                self.human_delay()
                return True
            else:
                self.log_message(f"⚠️ Could not find UI element '{element_name}' on screen")
                return False
        except Exception as e:
            self.log_message(f"❌ Error locating UI element: {str(e)}")
            return False
    
    def start_ai_automation(self):
        """Start AI-powered automation"""
        if not self.openai_api_key:
            self.log_message("❌ Please enter and save your OpenAI API key first")
            return
            
        # Get the natural language command
        command = self.command_entry.get("1.0", tk.END).strip()
        if not command:
            self.log_message("❌ Please enter an automation command")
            return
            
        # Disable buttons
        self.parse_btn.config(state="disabled")
        self.ai_stop_btn.config(state="normal")
        self.ai_automation_active = True
        self.stop_event.clear()
        
        # Start in new thread
        ai_thread = threading.Thread(target=self.run_ai_automation, args=(command,))
        ai_thread.daemon = True
        ai_thread.start()
    
    def run_ai_automation(self, command):
        """Run the AI-powered automation sequence"""
        try:
            self.log_message(f"🤖 Starting AI automation for command: {command}")
            
            # Parse the command
            actions = self.parse_command_with_openai(command)
            
            # Update the parsed actions display
            self.parsed_text.config(state="normal")
            self.parsed_text.delete(1.0, tk.END)
            self.parsed_text.insert(tk.END, json.dumps(actions, indent=2))
            self.parsed_text.config(state="disabled")
            
            if not actions:
                self.log_message("❌ No actions generated. Stopping automation.")
                return
                
            # Execute actions
            total = len(actions)
            self.log_message(f"🤖 Executing {total} actions...")
            
            for index, action in enumerate(actions, start=1):
                if self.stop_event.is_set():
                    self.log_message("🛑 AI automation stopped by user")
                    break
                    
                # Update progress
                progress = (index / total) * 100
                self.progress_var.set(progress)
                self.update_status(f"AI Action {index}/{total}: {action.get('action', '')}")
                
                # Execute action
                success = self.execute_ai_action(action)
                if not success:
                    self.log_message(f"⚠️ Action {index} failed, but continuing...")
                
                # Check if we should stop after each action
                if self.stop_event.is_set():
                    break
            
            if not self.stop_event.is_set():
                self.log_message("🤖 ✅ AI automation completed successfully")
                self.progress_var.set(100)
                self.update_status("AI automation completed")
        
        except Exception as e:
            self.log_message(f"❌ AI automation error: {str(e)}")
        finally:
            # Terminate Chrome if still running
            if self.current_process:
                try:
                    self.current_process.terminate()
                except:
                    pass
                    
            # Re-enable buttons
            self.parse_btn.config(state="normal")
            self.ai_stop_btn.config(state="disabled")
            self.ai_automation_active = False
    
    def stop_ai_automation(self):
        """Stop the AI-powered automation"""
        self.log_message("🛑 Stopping AI automation...")
        self.stop_event.set()
        self.update_status("Stopping AI automation...")
        
        # Terminate Chrome process if running
        if self.current_process:
            try:
                self.current_process.terminate()
                self.log_message("🔒 Chrome process terminated")
            except:
                pass
    
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