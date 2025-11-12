# Runtime hook to fix DLL loading issues
import sys
import os

# Create a fake pkg_resources module to prevent import errors
# Do this BEFORE any other imports to prevent PyInstaller's hook from running
class FakePkgResources:
    """Fake pkg_resources module"""
    working_set = []
    def __getattr__(self, name):
        return lambda *a, **k: None

# Install fake module early
if 'pkg_resources' not in sys.modules:
    sys.modules['pkg_resources'] = FakePkgResources()

# CRITICAL: Import SSL early before webview tries to import it
# This ensures SSL DLLs are loaded before any other module tries to use them
try:
    import _ssl  # Import the C extension directly first
    import ssl   # Then import the Python wrapper
    # Test that SSL is working
    ssl.create_default_context()
except Exception as e:
    pass  # Continue anyway, might work without SSL for basic functionality

# Fix DLL loading for _ssl.pyd and other extensions
# This MUST run BEFORE any SSL imports
# Add the temp directory to DLL search path for onefile builds
if hasattr(sys, '_MEIPASS'):
    # We're in a PyInstaller onefile bundle
    temp_dir = sys._MEIPASS
    
    # CRITICAL: Set DLL directory FIRST before any imports
    # Method 1: Use Windows API to set DLL directory (runs before PATH)
    try:
        import ctypes
        from ctypes import wintypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetDllDirectoryW.argtypes = [wintypes.LPCWSTR]
        kernel32.SetDllDirectoryW.restype = wintypes.BOOL
        result = kernel32.SetDllDirectoryW(temp_dir)
        # Silent success - no print needed
    except Exception as e:
        pass
    
    # Method 2: Add temp directory to PATH environment variable
    current_path = os.environ.get('PATH', '')
    if temp_dir not in current_path:
        os.environ['PATH'] = temp_dir + os.pathsep + current_path
    
    # Method 3: Use os.add_dll_directory (Python 3.8+ on Windows)
    if hasattr(os, 'add_dll_directory'):
        try:
            os.add_dll_directory(temp_dir)
        except Exception as e:
            pass
    
    # Also add webview lib directory to PATH if it exists
    webview_lib_dir = os.path.join(temp_dir, 'webview', 'lib')
    if os.path.exists(webview_lib_dir):
        if webview_lib_dir not in current_path:
            os.environ['PATH'] = webview_lib_dir + os.pathsep + os.environ.get('PATH', '')
        try:
            if hasattr(os, 'add_dll_directory'):
                os.add_dll_directory(webview_lib_dir)
        except Exception:
            pass

