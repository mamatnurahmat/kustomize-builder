@echo off
echo Starting Kustomize Builder Web App...
echo.
echo Make sure you have Python and Kustomize installed!
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting the application...
echo Open your browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the application
echo.
python app.py
pause 