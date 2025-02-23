@echo off
echo building main.py and others.
del /f /q dist
del /f /q build
del /f /q __pycache__
pyinstaller main.spec
echo building installer.py and others.
pyinstaller installer.spec
move /Y C:\Users\light\Documents\Ai-Assistant\dist\installer.exe C:\Users\light\Documents\Ai-Assistant\installer.exe
pause