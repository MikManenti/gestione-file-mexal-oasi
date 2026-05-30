@echo off
setlocal

REM Crea un ambiente virtuale locale
if not exist .venv (
    py -m venv .venv
    if errorlevel 1 goto :error
)

call .venv\Scripts\activate
if errorlevel 1 goto :error

python -m pip install --upgrade pip
if errorlevel 1 goto :error

python -m pip install -r requirements.txt
if errorlevel 1 goto :error

REM Build .exe singolo senza console
python -m PyInstaller --noconfirm --onefile --windowed --name ConvertitoreCSV converter_gui.py
if errorlevel 1 goto :error

echo.
echo Build completata. Trovi l'eseguibile in dist\ConvertitoreCSV.exe
pause
exit /b 0

:error
echo.
echo Build non riuscita. Correggi gli errori sopra e riprova.
pause
exit /b 1
