@echo off
REM filepath: c:\Users\richa\OneDrive\Documents\Github_Richard_Helms\salesforce-deployer\salesforce-deployer\setup-api-tools.bat

echo ===================================================
echo Salesforce Deployer API Tools Setup
echo ===================================================
echo.

REM Create a temporary PowerShell script file
echo $PROJECT_ROOT = 'C:\Users\richa\OneDrive\Documents\Github_Richard_Helms\salesforce-deployer\salesforce-deployer' > temp_script.ps1
echo $API_SPEC = Join-Path $PROJECT_ROOT 'api-specs\v1\salesforce-deployer-api.yaml' >> temp_script.ps1
echo $TESTS_DIR = Join-Path $PROJECT_ROOT 'tests' >> temp_script.ps1
echo $API_TESTS_DIR = Join-Path $TESTS_DIR 'integration\api' >> temp_script.ps1
echo $UNIT_TESTS_DIR = Join-Path $TESTS_DIR 'unit\api' >> temp_script.ps1
echo $TEMP_API_DIR = Join-Path $PROJECT_ROOT 'src\api' >> temp_script.ps1
echo. >> temp_script.ps1

echo Write-Host 'Step 1: Validating API Specification...' >> temp_script.ps1
echo spectral lint $API_SPEC >> temp_script.ps1
echo. >> temp_script.ps1

echo Write-Host 'Step 2: Generating FastAPI code...' >> temp_script.ps1
echo openapi-generator-cli generate -i $API_SPEC -g python-fastapi -o $TEMP_API_DIR >> temp_script.ps1
echo. >> temp_script.ps1

echo Write-Host 'Step 3: Moving test files to proper location...' >> temp_script.ps1
echo New-Item -Path $API_TESTS_DIR -ItemType Directory -Force >> temp_script.ps1
echo New-Item -Path $UNIT_TESTS_DIR -ItemType Directory -Force >> temp_script.ps1
echo New-Item -Path (Join-Path $PROJECT_ROOT 'src\api\routes') -ItemType Directory -Force >> temp_script.ps1
echo New-Item -Path (Join-Path $PROJECT_ROOT 'src\models') -ItemType Directory -Force >> temp_script.ps1
echo. >> temp_script.ps1

echo Copy-Item -Path (Join-Path $TEMP_API_DIR 'src\openapi_server\apis\*.py') -Destination (Join-Path $PROJECT_ROOT 'src\api\routes') -Force >> temp_script.ps1
echo Copy-Item -Path (Join-Path $TEMP_API_DIR 'src\openapi_server\models\*.py') -Destination (Join-Path $PROJECT_ROOT 'src\models') -Force >> temp_script.ps1
echo Copy-Item -Path (Join-Path $TEMP_API_DIR 'src\openapi_server\main.py') -Destination (Join-Path $PROJECT_ROOT 'src\api\app.py') -Force >> temp_script.ps1
echo Copy-Item -Path (Join-Path $TEMP_API_DIR 'tests\*.py') -Destination $API_TESTS_DIR -Force >> temp_script.ps1
echo Set-Content -Path (Join-Path $API_TESTS_DIR '__init__.py') -Value '# API Tests' >> temp_script.ps1
echo Set-Content -Path (Join-Path $UNIT_TESTS_DIR '__init__.py') -Value '# API Unit Tests' >> temp_script.ps1
echo. >> temp_script.ps1

echo Write-Host 'Step 4: Starting mock server in a new window...' >> temp_script.ps1
echo Start-Process powershell -ArgumentList '-Command', "prism mock '$API_SPEC' --cors" >> temp_script.ps1
echo. >> temp_script.ps1

echo Write-Host 'Step 5: Creating test HTML interface...' >> temp_script.ps1
echo $htmlContent = @' >> temp_script.ps1
echo ^<!DOCTYPE html^> >> temp_script.ps1
echo ^<html lang="en"^> >> temp_script.ps1
echo ^<head^> >> temp_script.ps1
echo     ^<meta charset="UTF-8"^> >> temp_script.ps1
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^> >> temp_script.ps1
echo     ^<title^>Salesforce Deployer API Tester^</title^> >> temp_script.ps1
echo     ^<style^> >> temp_script.ps1
echo         body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; } >> temp_script.ps1
echo         button { margin: 10px 0; padding: 8px 16px; } >> temp_script.ps1
echo         pre { background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; } >> temp_script.ps1
echo     ^</style^> >> temp_script.ps1
echo ^</head^> >> temp_script.ps1
echo ^<body^> >> temp_script.ps1
echo     ^<h1^>Salesforce Deployer API Tester^</h1^> >> temp_script.ps1
echo     ^<p^>Use these buttons to test the mock API endpoints:^</p^> >> temp_script.ps1
echo. >> temp_script.ps1
echo     ^<h2^>Authentication^</h2^> >> temp_script.ps1
echo     ^<button onclick="loginTest()"^>Test Login^</button^> >> temp_script.ps1
echo     ^<pre id="login-result"^>Results will appear here...^</pre^> >> temp_script.ps1
echo. >> temp_script.ps1
echo     ^<h2^>Organizations^</h2^> >> temp_script.ps1
echo     ^<button onclick="getOrgsTest()"^>Get Organizations^</button^> >> temp_script.ps1
echo     ^<pre id="orgs-result"^>Results will appear here...^</pre^> >> temp_script.ps1
echo. >> temp_script.ps1
echo     ^<script^> >> temp_script.ps1
echo         let token = ''; >> temp_script.ps1
echo. >> temp_script.ps1
echo         async function loginTest() { >> temp_script.ps1
echo             const loginResult = document.getElementById('login-result'); >> temp_script.ps1
echo             try { >> temp_script.ps1
echo                 const response = await fetch('http://127.0.0.1:4010/api/v1/auth/login', { >> temp_script.ps1
echo                     method: 'POST', >> temp_script.ps1
echo                     headers: { >> temp_script.ps1
echo                         'Content-Type': 'application/json' >> temp_script.ps1
echo                     }, >> temp_script.ps1
echo                     body: JSON.stringify({ >> temp_script.ps1
echo                         username: 'user@example.com', >> temp_script.ps1
echo                         password: 'myPassword123' >> temp_script.ps1
echo                     }) >> temp_script.ps1
echo                 }); >> temp_script.ps1
echo                 const data = await response.json(); >> temp_script.ps1
echo                 token = data.accessToken; >> temp_script.ps1
echo                 loginResult.textContent = JSON.stringify(data, null, 2); >> temp_script.ps1
echo             } catch (error) { >> temp_script.ps1
echo                 loginResult.textContent = `Error: ${error.message}`; >> temp_script.ps1
echo             } >> temp_script.ps1
echo         } >> temp_script.ps1
echo. >> temp_script.ps1
echo         async function getOrgsTest() { >> temp_script.ps1
echo             const orgsResult = document.getElementById('orgs-result'); >> temp_script.ps1
echo             try { >> temp_script.ps1
echo                 const response = await fetch('http://127.0.0.1:4010/api/v1/organizations', { >> temp_script.ps1
echo                     headers: { >> temp_script.ps1
echo                         'Authorization': `Bearer ${token || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}` >> temp_script.ps1
echo                     } >> temp_script.ps1
echo                 }); >> temp_script.ps1
echo                 const data = await response.json(); >> temp_script.ps1
echo                 orgsResult.textContent = JSON.stringify(data, null, 2); >> temp_script.ps1
echo             } catch (error) { >> temp_script.ps1
echo                 orgsResult.textContent = `Error: ${error.message}`; >> temp_script.ps1
echo             } >> temp_script.ps1
echo         } >> temp_script.ps1
echo     ^</script^> >> temp_script.ps1
echo ^</body^> >> temp_script.ps1
echo ^</html^> >> temp_script.ps1
echo '@ >> temp_script.ps1
echo. >> temp_script.ps1

echo Set-Content -Path (Join-Path $PROJECT_ROOT 'test-api.html') -Value $htmlContent >> temp_script.ps1
echo. >> temp_script.ps1

echo Start-Process (Join-Path $PROJECT_ROOT 'test-api.html') >> temp_script.ps1
echo. >> temp_script.ps1

echo Write-Host 'Setup Complete! Open test-api.html to test your API endpoints.' >> temp_script.ps1
echo. >> temp_script.ps1

REM Run the temporary PowerShell script
powershell.exe -ExecutionPolicy Bypass -File temp_script.ps1

REM Clean up the temporary PowerShell script file
del temp_script.ps1

echo.
echo If any errors occurred, try running the PowerShell script directly:
echo powershell -ExecutionPolicy Bypass -File setup-api-tools.ps1
echo.
pause