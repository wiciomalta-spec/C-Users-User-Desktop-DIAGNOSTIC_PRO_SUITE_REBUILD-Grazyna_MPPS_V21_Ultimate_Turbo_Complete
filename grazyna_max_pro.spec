# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\User\\Desktop\\DIAGNOSTIC_PRO_SUITE_REBUILD\\Grazyna_MPPS_V21_Ultimate_Turbo_Complete\\grazyna_max_pro.py'],
    pathex=[],
    binaries=[('C:\\Program Files\\dotnet\\packs\\Microsoft.iOS.Windows.Sdk.net9.0_18.0\\18.0.9617\\tools\\msbuild\\iOS\\imobiledevice-x64\\libusb-1.0.dll', '.')],
    datas=[('C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pyfiglet\\fonts', 'pyfiglet/fonts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GRAZYNA_MAX_PRO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
