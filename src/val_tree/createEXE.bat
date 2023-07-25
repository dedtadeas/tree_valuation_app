@echo off
setlocal

set PY_PATH=%~dp0Env\Scripts\python.exe
set PYINSTALLER_PATH=%~dp0Env\Scripts\pyinstaller.exe
set SCRIPT_PATH=%~dp0Hodnota_stromu.py
set ICON_PATH=%~dp0imgs\icon.ico
set IMG_PATH=%~dp0imgs\*.*

"%PYINSTALLER_PATH%" -F -w --add-data "%IMG_PATH%;imgs/." --hidden-import openpyxl.cell._writer --icon="%ICON_PATH%" "%SCRIPT_PATH%"

endlocal





pyinstaller -F -w --add-data "imgs/*.*;imgs/." --hidden-import openpyxl.cell._writer --icon=imgs/icon.ico Hodnota_stromu.py