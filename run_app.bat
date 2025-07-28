@echo off
setlocal
cls
echo ---------------------------------------------
echo   Stonehaven CLI Launcher
echo ---------------------------------------------

:: Handle optional --debug flag
if "%1"=="--debug" (
    echo [INFO] Launching in DEBUG mode...
    python main.py --debug
) else (
    python main.py
)

:: Show exit status
if errorlevel 1 (
    echo [ERROR] Application exited with errors.
) else (
    echo [OK] Application closed successfully.
)

pause
