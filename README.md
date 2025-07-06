# AI-Powered Website Automation Bot

A cutting-edge desktop application that combines traditional website automation with advanced AI-driven natural language command processing. Built with Python and Tkinter, this tool empowers users to automate complex web interactions effortlessly.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Configuration Tab](#configuration-tab)
  - [AI Commands Tab](#ai-commands-tab)
  - [Execution Log Tab](#execution-log-tab)
  - [About Tab](#about-tab)
- [Example AI Command](#example-ai-command)
- [Troubleshooting](#troubleshooting)
- [Developer](#developer)
- [License](#license)

---

## Features

- Intuitive multi-tab GUI for seamless automation setup and monitoring.
- Supports visiting multiple websites (up to 50 URLs).
- Automates mouse clicks, scrolling, mouse movements, and screenshots.
- Website content keyword checking and reading capabilities.
- AI-powered natural language command parsing using OpenAI GPT-4 Turbo.
- UI element recognition via image matching for precise interactions.
- Real-time execution logging with color-coded messages.
- Progress tracking with visual progress bar and status updates.
- Cross-platform compatibility (Windows, macOS, Linux).
- Launches Google Chrome in incognito mode for privacy during automation.

---

## Installation

### Prerequisites

- Python 3.8 or higher installed on your system.
- Google Chrome browser installed.
- OpenAI API key (required for AI features).

### Setup Steps

1. **Clone or download the repository** to your local machine.

2. **Install required Python packages**:

   ```bash
   pip install pyautogui requests beautifulsoup4 Pillow openai
   ```

3. **Run the application**:

   ```bash
   python main.py
   ```

---

## Usage

### Configuration Tab

- **Websites to Visit**: Enter one URL per line (maximum 50). Example URLs are pre-filled for convenience.
- **Timing Settings**:
  - *Page Load Time*: Seconds to wait for each page to load.
  - *Work Time per Site*: Duration to perform automated actions on each site.
- **Automation Tasks**: Select which actions to perform:
  - Mouse Click, Scroll Page, Mouse Movement, Take Screenshot, Check Website, Read Content.
- **Content Check Options**: Specify a keyword to search for on each website.
- **Control Buttons**:
  - *Start Automation*: Begins the automation process.
  - *Stop*: Halts the automation immediately.
- **Progress Bar and Status**: Visual indicators of automation progress and current status.

### AI Commands Tab

- **OpenAI API Settings**: Enter and save your OpenAI API key to enable AI features.
- **UI Element Recognition**: Upload images of UI elements (buttons, icons) for the bot to recognize and interact with.
- **Natural Language Commands**: Describe your automation task in plain English.
- **Parse & Run**: Converts your command into actionable steps and executes them.
- **Stop AI**: Immediately stops AI-driven automation.

### Execution Log Tab

- Displays real-time logs of all automation activities, including successes, errors, AI responses, and system messages.
- Use *Clear Log* button to reset the log view.

### About Tab

- Provides detailed information about the application, its features, and the developer.

---

## Example AI Command

```
Visit example.com, search for 'automation tools', click the search button, wait 5 seconds, and take a screenshot
```

---

## Troubleshooting

- **Chrome Not Found**: Ensure Google Chrome is installed in the default location or update the path in the code.
- **OpenAI API Errors**: Verify your API key is correct and has sufficient quota.
- **UI Element Not Found**: Upload clear, high-quality images of UI elements for recognition.
- **Automation Stops Unexpectedly**: Check the log for error messages and ensure no conflicting processes are running.

---

## Developer

Nayan Ray  
Release Date: July 2025  
License: MIT Open Source

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
