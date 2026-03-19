# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['C:\\Users\\User\\PycharmProjects\\AlaCart\\main\\Alacarte.py'],  # Path to your entry script
    pathex=['.'],      # Look in the current root directory for modules
    binaries=[],
    datas=[
        ('res', 'res'),           # Include the entire 'res' folder
        ('Database', 'Database'), # Include the 'Database' folder
    ],
    hiddenimports=[
        'ui',
        'util',
        'dataManager'
    ], # Explicitly list modules if they aren't being detected
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='AlaCart',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Set to True if you need to see terminal errors for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['res/icon.png'], # Optional: path to your icon
)
