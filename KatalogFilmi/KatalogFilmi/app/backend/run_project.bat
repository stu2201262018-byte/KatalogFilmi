@echo off
REM Активиране на виртуалната среда
call .venv\Scripts\activate.bat

REM Стартира Flask сървъра в отделен прозорец
start cmd /k "python app\backend\app.py"

REM Изчакване 2 секунди, за да се стартира сървъра
timeout /t 2 >nul

REM Отваряне на браузъра на правилния линк
start http://127.0.0.1:5000/api/movies

pause
