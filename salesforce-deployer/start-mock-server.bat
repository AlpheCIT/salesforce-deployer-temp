@echo off
REM filepath: c:\Users\richa\OneDrive\Documents\Github_Richard_Helms\salesforce-deployer\salesforce-deployer\start-mock-server.bat

echo Starting Salesforce Deployer Mock API Server...
echo.

REM Check if Prism is installed
where prism >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Prism CLI not found. Installing...
    npm install -g @stoplight/prism-cli
)

echo.
echo Starting Prism mock server in the background...
start /b cmd /c "prism mock api-specs/v1/salesforce-deployer-api.yaml --cors"

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo.
echo Opening API test page in default browser...
start "" "test.html"

echo.
echo Mock server is running at http://127.0.0.1:4010
echo.
echo Press Ctrl+C in the server window to stop the mock server when finished.
echo.

REM Keep the window open
pause