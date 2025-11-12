# clipnotes

A clean, minimalist desktop sticky notes application similar to Windows Sticky Notes.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)

## Features

- 🎨 9 color options for notes
- 📝 Full-screen writing area for maximum focus
- ➕ Easy note creation with + button
- 🔄 Navigate between multiple notes (Previous/Next)
- ✏️ Edit notes with dedicated edit button
- 💾 Auto-save functionality
- 🗑️ Delete individual notes
- ⌨️ Keyboard shortcuts (Ctrl+N for new note)
- 🎯 Clean, distraction-free interface with floating header
- 💻 Portable executable - no installation required

## Installation

### Option 1: Portable Executable (Recommended)

1. Download `clipnotes.exe` from [Releases](https://github.com/H-ProjectX/clipnotes/releases)
2. Run `clipnotes.exe` directly - no installation needed!
3. Your notes are saved in `notes-data.json` in the same folder as the executable

### Option 2: Installer

1. Download `clipnotes_installer.exe` from [Releases](https://github.com/H-ProjectX/clipnotes/releases)
2. Run the installer
3. Launch from Start Menu or Desktop shortcut

## Usage

- **Create note**: Click **+** button or press `Ctrl+N`
- **Edit note**: Click **✎** button or double-click the note text
- **Change color**: Click color dots in the header
- **Navigate**: Use **◀** button to go to previous note (when multiple notes exist)
- **Delete note**: Click **×** button in header
- **Save note**: Click **✓** button or click outside the text area
- **Full-screen writing**: The entire screen is dedicated to writing - header appears on hover

## Building from Source

### Requirements

- Python 3.8+
- pip
- Windows 10/11

### Steps

```bash
# Clone repository
git clone https://github.com/H-ProjectX/clipnotes.git
cd clipnotes

# Install dependencies
pip install -r requirements.txt

# Build executable
build_exe.bat

# The executable will be created in dist\clipnotes.exe
```

### Building Installer (Optional)

1. Install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Run `create_installer.bat` or manually compile `installer.iss`

## Project Structure

```
clipnotes/
├── app.py                      # Main Python application
├── desktop-sticky-notes.html   # HTML/JavaScript UI
├── clipnotes.spec              # PyInstaller configuration
├── build_exe.bat               # Build script
├── requirements.txt            # Python dependencies
├── icon.ico                    # Application icon
└── dist/                       # Build output directory
    └── clipnotes.exe          # Compiled executable
```

## Data Storage

- Notes are saved in `notes-data.json` in the same directory as the executable
- Data persists between sessions automatically
- Portable: Move the exe and data file together to keep your notes

## Requirements

- Windows 10/11
- WebView2 Runtime (usually pre-installed with Windows)

## Keyboard Shortcuts

- `Ctrl+N` - Create a new note
- `Esc` - Exit edit mode (when editing a note)

## Color Options

The app includes 9 color themes:
- White (default)
- Yellow
- Orange
- Green
- Blue
- Purple
- Red
- Teal
- Pink

## Troubleshooting

### Application won't start
- Ensure WebView2 Runtime is installed (usually comes with Windows)
- Try running as administrator

### Notes not saving
- Check that the application has write permissions in the folder
- Ensure `notes-data.json` is not read-only

### Build issues
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure PyInstaller is up to date: `pip install --upgrade pyinstaller`

## Development

### Running from Source

```bash
python app.py
```

### Debug Mode

To enable debug mode (opens DevTools), edit `app.py`:
```python
webview.start(debug=True)  # Change False to True
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

H-ProjectX
