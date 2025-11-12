# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_dynamic_libs

block_cipher = None

# Collect webview and SSL dependencies
datas = [('desktop-sticky-notes.html', '.'), ('icon.ico', '.')]
binaries = []
hiddenimports = [
    'webview',
    'webview.platforms',
    'webview.platforms.winforms',
    'webview.platforms.edgechromium',
    'webview.platforms.mshtml',
    'webview.js',
    'webview.js.bottle',
    'webview.js.django',
    'webview.js.flask',
    'ssl',
    '_ssl',
    '_hashlib',
    '_socket',
    'ctypes',
    'ctypes.wintypes',
]

# Collect webview data files and binaries
try:
    webview_datas, webview_binaries, webview_hiddenimports = collect_all('webview')
    datas += webview_datas
    binaries += webview_binaries
    hiddenimports += webview_hiddenimports
    print("Collected webview files via collect_all")
except Exception as e:
    print(f"Warning collecting webview: {e}")

# Collect all SSL-related files
try:
    ssl_datas, ssl_binaries, ssl_hiddenimports = collect_all('ssl')
    datas += ssl_datas
    binaries += ssl_binaries
    hiddenimports += ssl_hiddenimports
    print("Collected SSL files via collect_all")
except Exception as e:
    print(f"Warning collecting SSL: {e}")

# Collect SSL dynamic libraries
try:
    ssl_dyn = collect_dynamic_libs('ssl')
    binaries += ssl_dyn
    print("Collected SSL dynamic libraries")
except Exception as e:
    print(f"Warning collecting SSL dynamic libs: {e}")

# Find and explicitly include Python DLLs
python_dlls_dir = None
possible_dll_dirs = [
    os.path.join(os.path.dirname(sys.executable), 'DLLs'),
    os.path.join(sys.prefix, 'DLLs'),
    os.path.join(sys.exec_prefix, 'DLLs'),
]

for dll_dir in possible_dll_dirs:
    if os.path.exists(dll_dir):
        python_dlls_dir = dll_dir
        print(f"Found Python DLLs at: {python_dlls_dir}")
        break

# Collect existing binary names
existing_names = [os.path.basename(b[0]) if isinstance(b, tuple) else os.path.basename(b) for b in binaries]

# OpenSSL DLL names to search for
openssl_names = ['libssl-1_1.dll', 'libcrypto-1_1.dll', 'libssl-3.dll', 'libcrypto-3.dll', 
                 'libssl-1_1-x64.dll', 'libcrypto-1_1-x64.dll']

if python_dlls_dir:
    # Include required .pyd files
    required_pyds = ['_ssl.pyd', '_hashlib.pyd', '_socket.pyd', 'pyexpat.pyd', '_ctypes.pyd']
    
    for pyd_name in required_pyds:
        pyd_path = os.path.join(python_dlls_dir, pyd_name)
        if os.path.exists(pyd_path) and pyd_name not in existing_names:
            binaries.append((pyd_path, '.'))
            existing_names.append(pyd_name)
            print(f"Added: {pyd_name} from {pyd_path}")
    
    # Find OpenSSL DLLs in Python installation
    python_root = os.path.dirname(sys.executable)
    
    # Check in Python root
    for dll_name in openssl_names:
        dll_path = os.path.join(python_root, dll_name)
        if os.path.exists(dll_path) and dll_name not in existing_names:
            binaries.append((dll_path, '.'))
            existing_names.append(dll_name)
            print(f"Added OpenSSL DLL from Python root: {dll_name}")
    
    # Check in DLLs directory
    for dll_name in openssl_names:
        dll_path = os.path.join(python_dlls_dir, dll_name)
        if os.path.exists(dll_path) and dll_name not in existing_names:
            binaries.append((dll_path, '.'))
            existing_names.append(dll_name)
            print(f"Added OpenSSL DLL from DLLs: {dll_name}")

# Miniconda-specific path for OpenSSL DLLs
miniconda_library_bin = os.path.join(sys.prefix, 'Library', 'bin')
if os.path.exists(miniconda_library_bin):
    print(f"Checking Miniconda Library\\bin: {miniconda_library_bin}")
    for dll_name in openssl_names:
        dll_path = os.path.join(miniconda_library_bin, dll_name)
        if os.path.exists(dll_path) and dll_name not in existing_names:
            binaries.append((dll_path, '.'))
            existing_names.append(dll_name)
            print(f"Added Miniconda OpenSSL DLL: {dll_name} from {dll_path}")

# Also check Library\lib (another Miniconda location)
miniconda_library_lib = os.path.join(sys.prefix, 'Library', 'lib')
if os.path.exists(miniconda_library_lib):
    for dll_name in openssl_names:
        dll_path = os.path.join(miniconda_library_lib, dll_name)
        if os.path.exists(dll_path) and dll_name not in existing_names:
            binaries.append((dll_path, '.'))
            existing_names.append(dll_name)
            print(f"Added OpenSSL DLL from Library\\lib: {dll_name}")

print(f"\nTotal binaries to include: {len(binaries)}")
print("SSL-related binaries:")
for b in binaries:
    bname = os.path.basename(b[0]) if isinstance(b, tuple) else os.path.basename(b)
    if 'ssl' in bname.lower() or 'crypto' in bname.lower() or '_ssl' in bname:
        print(f"  - {bname}")
print()

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=['pkg_resources'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='clipnotes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
