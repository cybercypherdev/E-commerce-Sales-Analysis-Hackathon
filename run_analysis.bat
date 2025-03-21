@echo off
echo ===================================
echo E-commerce Sales Analysis Pipeline
echo ===================================

echo.
echo Step 1: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Creating SQLite database...
python python/export_to_db.py

echo.
echo Step 3: Running SQL analysis...
python python/run_sql_analysis.py

echo.
echo Step 4: Running Python analysis...
python python/analysis.py

echo.
echo Step 5: Preparing Power BI data...
mkdir powerbi\data 2>nul
copy data\sql_results\*.csv powerbi\data\ /Y
copy data\python_results\*.png powerbi\images\ /Y

echo.
echo ===================================
echo Analysis Pipeline Complete!
echo.
echo Results can be found in:
echo - SQL Analysis: data\sql_results
echo - Python Analysis: data\python_results
echo - Power BI Data: powerbi\data
echo ===================================

pause 