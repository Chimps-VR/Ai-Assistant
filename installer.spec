# -*- mode: python ; coding: utf-8 -*-

import os  # Import os to use path joining

a = Analysis(
    ['installer.py'],
    pathex=[],
    binaries=[],
    datas=[('app.zip', '.'), ('Icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=['grp', 'pwd', 'posix', 'resource', '_frozen_importlib_external', '_posixsubprocess', 'fcntl'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# Modify the distpath and workpath to specify the 'installer' folder
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='installer',
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
    icon='Icon.ico'
)

