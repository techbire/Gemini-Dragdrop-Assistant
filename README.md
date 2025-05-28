
# Gemini Drag & Drop Assistant 🧠✨

A simple Python desktop tool that allows you to **drag and drop text**, query Google's **Gemini AI**, and get direct answers using keyboard shortcuts.

---

## 🚀 Features

- 🖱️ Drag-and-drop text UI using `TkinterDnD2`
- ⌨️ Hotkey control:
  - `Ctrl+Z` → Open Drop Window
  - `Ctrl+X` → Query Gemini AI
  - `Ctrl+C` → Close all windows
- 🤖 Direct answers with no explanation
- 🔐 Secure API key handling via `.env`

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/gemini-dragdrop-assistant.git
cd gemini-dragdrop-assistant
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup `.env` file

Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ Never commit this file. It’s already ignored via `.gitignore`.

---

## 📦 Requirements

* Python 3.7+
* `tkinterdnd2`
* `keyboard`
* `python-dotenv`
* `google-generativeai`

You can also install them manually:

```bash
pip install tkinterdnd2 keyboard python-dotenv google-generativeai
```

---

## 🧠 How It Works

1. Hit `Ctrl+Z` to open the drag-and-drop box.
2. Drop some text (MCQ, prompt, question).
3. Hit `Ctrl+X` to get Gemini's direct answer.
4. Use `Ctrl+C` to close all windows.
