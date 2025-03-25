@echo off
echo ===================================
echo E-commerce Sales Analysis Pipeline
echo ===================================

echo.
echo Step 1: Installing Python dependencies...
pip install pandas numpy openpyxl sqlite3 matplotlib seaborn scikit-learn

echo.
echo Step 2: Running data validation...
python python/data_validation.py

echo.
echo Step 3: Running customer frequency analysis...
python python/customer_frequency_analysis.py

echo.
echo Step 4: Exporting data to database...
python python/export_to_db.py

echo.
echo Step 5: Running SQL analysis...
python python/run_sql_analysis.py

echo.
echo Step 6: Running Python analysis...
python python/analysis.py

echo.
echo Step 7: Preparing data for Power BI...
python python/prepare_powerbi_data.py

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