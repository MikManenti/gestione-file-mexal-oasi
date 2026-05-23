@echo off
setlocal

REM Crea un ambiente virtuale locale
if not exist .venv (
    py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Build .exe singolo senza console
pyinstaller --noconfirm --onefile --windowed --name ConvertitoreCSV converter_gui.py

echo.
echo Build completata. Trovi l'eseguibile in dist\ConvertitoreCSV.exe
pause
