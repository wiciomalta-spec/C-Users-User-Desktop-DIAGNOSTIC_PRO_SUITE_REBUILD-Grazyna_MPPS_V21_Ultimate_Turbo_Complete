# -*- mode: python ; coding: utf-8 -*-
import os, glob
from PyInstaller.utils.hooks import collect_data_files

project_path = os.path.abspath(os.getcwd())
script = 'grazyna_max_pro.py'

hidden_imports = [
    'usb','usb.core','usb.util',
    'serial','serial.tools.list_ports',
    'rich','pyfiglet','colorama',
    'pkg_resources','importlib_metadata'
]

# dołącz dane pyfiglet (czcionki)
datas = collect_data_files('pyfiglet')

# dołącz numpy.libs jeśli potrzebne
binaries = []
try:
    import numpy
    numpy_libs = os.path.join(os.path.dirname(numpy.__file__), '.libs')
    if os.path.isdir(numpy_libs):
        for f in glob.glob(os.path.join(numpy_libs, '*')):
            binaries.append((f, 'numpy.libs'))
except Exception:
    pass

# dołącz libusb-1.0.dll jeśli skopiowany do katalogu projektu
libusb_local = os.path.join(project_path, 'libusb-1.0.dll')
if os.path.exists(libusb_local):
    binaries.append((libusb_local, '.'))

a = Analysis([os.path.join(project_path, script)],
             pathex=[project_path],
             binaries=binaries,
             datas=datas,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
          name='grazyna_max_pro', debug=False, strip=False,
          upx=False, console=True, icon=None)
