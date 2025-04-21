@echo off
REM filepath: c:\Users\richa\OneDrive\Documents\Github_Richard_Helms\salesforce-deployer\salesforce-deployer\generate-api-code.bat

echo Generating FastAPI code from OpenAPI specification...
echo.

REM Check if OpenAPI Generator CLI is installed
where openapi-generator-cli >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo OpenAPI Generator CLI not found. Installing...
    call npm install -g @openapitools/openapi-generator-cli
)

echo.
echo Generating Python FastAPI code...
openapi-generator-cli generate -i api-specs/v1/salesforce-deployer-api.yaml -g python-fastapi -o temp_api/

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Code generation completed successfully!
    
    REM Create directories if they don't exist
    if not exist "src\api\routes" mkdir src\api\routes
    if not exist "src\models" mkdir src\models
    
    REM Move files to proper locations
    echo Moving files to proper project structure...
    xcopy /Y /I "temp_api\src\openapi_server\apis\*.py" "src\api\routes\"
    xcopy /Y /I "temp_api\src\openapi_server\models\*.py" "src\models\"
    copy /Y "temp_api\src\openapi_server\main.py" "src\api\app.py"
    
    REM Copy test files
    echo Moving test files...
    if not exist "tests\integration\api" mkdir tests\integration\api
    xcopy /Y /I "temp_api\tests\*.py" "tests\integration\api\"
    
    REM Clean up temporary files
    echo Cleaning up temporary files...
    rmdir /S /Q temp_api
    
    echo Generated code has been reorganized to the proper project structure.
) else (
    echo.
    echo Error generating code. Please check your API specification.
)

echo.
pause