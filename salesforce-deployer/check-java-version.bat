@echo off
REM filepath: c:\Users\richa\OneDrive\Documents\Github_Richard_Helms\salesforce-deployer\salesforce-deployer\check-java-version.bat

echo Checking Java version for OpenAPI Generator compatibility...
echo.

REM Check if Java is installed
java -version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Java is not installed. Please install Java 11 or higher.
    echo Download from: https://adoptium.net/temurin/releases/
    echo.
    pause
    start https://adoptium.net/temurin/releases/
    exit /b 1
)

REM Get Java version and store it in a temporary file
java -version 2> java_version.tmp

REM Extract the version number
set "javaversion="
for /f "tokens=3" %%a in (java_version.tmp) do (
    if not defined javaversion (
        set "javaversion=%%a"
    )
)

REM Clean up the version string (remove quotes)
set javaversion=%javaversion:"=%
echo Detected Java version: %javaversion%
echo.

REM Delete temporary file
del java_version.tmp

REM Simple check if version starts with 1.8
echo %javaversion% | findstr /b "1.8" >nul
if %ERRORLEVEL% EQU 0 (
    echo WARNING: You have Java 8 installed, but OpenAPI Generator requires Java 11 or higher.
    echo Please install a newer version of Java from: https://adoptium.net/temurin/releases/
    echo.
    pause
    start https://adoptium.net/temurin/releases/
    exit /b 1
)

REM Check version string starts with a number less than 11 (simple check)
for /f "tokens=1 delims=." %%a in ("%javaversion%") do set "majorversion=%%a"
if %majorversion% LSS 11 (
    echo WARNING: Your Java version %javaversion% is too old. OpenAPI Generator requires Java 11 or higher.
    echo Please install a newer version of Java from: https://adoptium.net/temurin/releases/
    echo.
    pause
    start https://adoptium.net/temurin/releases/
    exit /b 1
)

echo Your Java version %javaversion% is compatible with OpenAPI Generator.
echo.
pause
exit /b 0