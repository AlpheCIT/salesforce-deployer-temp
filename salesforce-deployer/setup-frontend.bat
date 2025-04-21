@echo off
REM filepath: c:\Users\richa\OneDrive\Documents\Github_Richard_Helms\salesforce-deployer\salesforce-deployer\setup-frontend.bat

echo ===================================================
echo Salesforce Deployer Frontend Setup
echo ===================================================
echo.

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js/npm is required but not installed.
    echo Please install Node.js from: https://nodejs.org/
    echo.
    pause
    start https://nodejs.org/
    exit /b 1
)

echo Installing openapi-typescript-codegen...
call npm install -g openapi-typescript-codegen

echo.
echo Creating frontend structure...
mkdir frontend\src\api 2>nul

echo.
echo Generating TypeScript types from OpenAPI specification...
call openapi-typescript-codegen --input api-specs/v1/salesforce-deployer-api.yaml --output frontend/src/api

echo.
echo Frontend setup complete!
echo TypeScript types have been generated in frontend/src/api
echo.

pause