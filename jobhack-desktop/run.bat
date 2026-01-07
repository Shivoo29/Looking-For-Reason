@echo off
REM JobHack Desktop Quick Start Script (Windows)

echo ================================================================
echo               JOBHACK DESKTOP - QUICK START
echo ================================================================
echo.

REM Check Java
echo Checking Java version...
java -version >nul 2>&1
if errorlevel 1 (
    echo X Java not found. Please install Java 17 or higher.
    exit /b 1
)
echo + Java detected

REM Check Maven
echo Checking Maven...
mvn -version >nul 2>&1
if errorlevel 1 (
    echo X Maven not found. Please install Maven 3.6+
    exit /b 1
)
echo + Maven detected

REM Check API key
echo Checking Anthropic API key...
if "%ANTHROPIC_API_KEY%"=="" (
    echo ! ANTHROPIC_API_KEY not set
    echo   Set it with: set ANTHROPIC_API_KEY=your-key
    echo   Or configure in %USERPROFILE%\.jobhack\application.conf
) else (
    echo + API key configured
)

echo.
echo Building JobHack Desktop...
call mvn clean compile -q

if errorlevel 1 (
    echo X Build failed. Check errors above.
    exit /b 1
)

echo + Build successful
echo.
echo Starting JobHack Desktop...
echo ================================================================
echo.

call mvn javafx:run
