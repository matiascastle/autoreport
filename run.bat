@echo off
REM AutoReport - Quick Run Script for Windows

echo.
echo Starting AutoReport...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo Setup complete!
echo.
echo Opening AutoReport...
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit
streamlit run app.py

