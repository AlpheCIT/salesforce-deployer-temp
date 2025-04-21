@echo off
REM filepath: c:\Users\richa\OneDrive\Documents\Github_Richard_Helms\salesforce-deployer\salesforce-deployer\setup-tools.bat

echo Setting up development tools for Salesforce Deployer...
echo.

echo Checking for Java installation...
java -version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Java is required but not installed.
    echo.
    echo Please download and install Java from:
    echo https://adoptium.net/temurin/releases/
    echo.
    echo After installing Java, run this script again.
    echo.
    pause
    start https://adoptium.net/temurin/releases/
    exit /b 1
)

REM Install Spectral for API validation
echo Installing Spectral CLI...
call npm install -g @stoplight/spectral-cli

REM Install Prism for API mocking
echo Installing Prism CLI...
call npm install -g @stoplight/prism-cli

REM Install OpenAPI Generator CLI
echo Installing OpenAPI Generator CLI...
call npm install -g @openapitools/openapi-generator-cli

echo.
echo Tools installation complete!
echo.
echo You can now use:
echo   - spectral lint api-specs/v1/salesforce-deployer-api.yaml (for API validation)
echo   - prism mock api-specs/v1/salesforce-deployer-api.yaml (for API mocking)
echo   - openapi-generator-cli generate -i api-specs/v1/salesforce-deployer-api.yaml -g python-fastapi -o src/api/ (for code generation)
echo.

pause