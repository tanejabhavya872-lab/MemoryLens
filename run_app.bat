@echo off
cd /d C:\Users\lenovo\ai-memory-assistant
call venv\Scripts\activate.bat

start "MemoryLens API" cmd /k "call venv\Scripts\activate.bat && uvicorn src.api.main:app"
timeout /t 15

streamlit run src\ui\app.py