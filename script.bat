@echo off
:loop
poetry run python main.py
timeout /t 100000 /nobreak > NUL
goto loop
