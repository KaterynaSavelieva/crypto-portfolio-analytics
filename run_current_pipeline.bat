@echo off
cd /d "C:\Users\051066\Crypto Portfolio Analytics System"

set PYTHONPATH=%CD%

"C:\Users\051066\Crypto Portfolio Analytics System\.venv\Scripts\python.exe" etl\current\run_current_pipeline.py