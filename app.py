import webview
import os
import json
import sys
from pathlib import Path

# Get the directory where the executable is located
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys.executable).parent
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if hasattr(sys, '_MEIPASS'):
        HTML_FILE = Path(sys._MEIPASS) / 'desktop-sticky-notes.html'
    else:
        HTML_FILE = BASE_DIR / 'desktop-sticky-notes.html'
else:
    # Running as script
    BASE_DIR = Path(__file__).parent
    HTML_FILE = BASE_DIR / 'desktop-sticky-notes.html'

DATA_FILE = BASE_DIR / 'notes-data.json'

def load_notes():
    """Load notes from JSON file"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e), 'data': {'notes': [], 'nextId': 1}}
    return {'success': True, 'data': {'notes': [], 'nextId': 1}}

def save_notes(notes, next_id):
    """Save notes to JSON file"""
    try:
        data = {'notes': notes, 'nextId': next_id}
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def create_window():
    """Create and show the webview window"""
    # Get icon path
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            ICON_FILE = Path(sys._MEIPASS) / 'icon.ico'
        else:
            ICON_FILE = BASE_DIR / 'icon.ico'
    else:
        ICON_FILE = BASE_DIR / 'icon.ico'
    
    icon_path = str(ICON_FILE) if ICON_FILE.exists() else None
    
    # Note: pywebview doesn't support icon parameter directly in create_window
    # The icon will be set by PyInstaller when building the exe
    # Get screen dimensions for full-screen window
    import tkinter as tk
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    # Get HTML file path as URL for proper file input support
    html_path = HTML_FILE.resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    # Convert path to file URL (works on Windows and Unix)
    if sys.platform == 'win32':
        # Windows: file:///C:/path/to/file.html
        html_url = f"file:///{str(html_path).replace(chr(92), '/')}"
    else:
        # Unix: file:///path/to/file.html
        html_url = f"file://{html_path}"

    # Create window with file URL (needed for file input to work properly)
    window = webview.create_window(
        'clipnotes',
        url=html_url,  # Use file URL instead of HTML string for file input support
        width=screen_width,
        height=screen_height,
        min_size=(800, 600),
        resizable=True,
        frameless=False,
        fullscreen=False
    )
    
    # Expose Python functions to JavaScript
    window.expose(load_notes, save_notes)
    
    webview.start(debug=False)

if __name__ == '__main__':
    try:
        create_window()
    except Exception as e:
        import traceback
        error_msg = f"Error starting clipnotes: {e}\n{traceback.format_exc()}"
        print(error_msg)
        # Try to show error in a message box if possible
        try:
            import tkinter.messagebox as msgbox
            msgbox.showerror("clipnotes Error", error_msg)
        except:
            pass
        sys.exit(1)

