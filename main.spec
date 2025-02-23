# -*- mode: python ; coding: utf-8 -*-

import shutil
import msilib
import os
import uuid
import msilib.schema
import zipfile

# File to store product code for consistent upgrades
productCodeFile = "productCode.txt"

# Application Version
version = "0.0.1"

# --- File Copy Process ---
os.system("echo INFO: Copying default assistants.")

if os.path.exists("assistants"):
    if os.path.exists("dist/assistants"):
        os.system("echo WARNING: Folder already exists, deleting.")
        shutil.rmtree("dist/assistants")
    shutil.copytree("assistants", "dist/assistants")
    shutil.copy("ReadMe.txt", "dist/")
    os.system("echo INFO: Copied assistants.")
else:
    os.system("echo \n")
    os.system("echo ERROR: assistants folder doesn't exist!")
    os.system("echo \n")

# --- PyInstaller Build Process ---
# block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('Icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=['grp', 'pwd', 'posix', 'resource', '_frozen_importlib_external', '_posixsubprocess', 'fcntl'],
    noarchive=False,
    optimize=0,
)

# Create Python zip archive
pyz = PYZ(a.pure)

# Build EXE
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='main',
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
    icon='icon.ico',
)


os.system("echo INFO: Build completed, zipping EXE!")

def zip_folder(folder_path, zip_name):
    # Create a zip file with the specified name
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder and add all files and subdirectories to the zip file
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                # Get the full path to the file
                file_path = os.path.join(foldername, filename)
                # Add the file to the zip file, preserving the folder structure
                zipf.write(file_path, os.path.relpath(file_path, start=folder_path))

# Create zip
zip_folder("dist/", "app.zip")

# Create exe Installer
os.system("pyinstaller installer.spec")