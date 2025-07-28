@echo off
setlocal ENABLEEXTENSIONS
cls

:: ASCII-style header
echo ============================================================
echo             Stonehaven CLI Launcher - Windows
echo ============================================================

:: Optional debug mode handling
if "%1"=="--debug" (
    echo [INFO] Launching in DEBUG mode...
    python main.py --debug
) else (
    echo [INFO] Launching application...
    python main.py
)

:: Exit code capture and status display
set "EXIT_CODE=%ERRORLEVEL%"

echo.
if %EXIT_CODE% NEQ 0 (
    echo [ERROR] Application exited with error code: %EXIT_CODE%
) else (
    echo [ OK ] Application closed successfully.
)

echo ------------------------------------------------------------
echo   Press any key to exit the launcher...
echo ------------------------------------------------------------
pause >nul
endlocal
