import duckdb
from pathlib import Path

con = duckdb.connect()
con.execute(""" 
   CREATE VIEW companies AS
    SELECT *
    FROM read_csv_auto('data/raw/companies.csv')""")
print("Данные подключены")

query = """SELECT
    city,
    COUNT(*) AS company_count,
    SUM(employees) AS total_employees,
    ROUND(AVG(employees), 2) AS avg_employees,
    MAX(employees) AS max_employees
FROM companies
GROUP BY city
ORDER BY total_employees DESC"""
result = con.execute(query).fetchdf()
print("\nИтоговый аналитический отчет:")
print(result.to_string(index=False))

output_dir = Path("analytics/reports")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = (output_dir / "city_analytics.csv")
result.to_csv(output_file, index=False, encoding="utf-8-sig",)
print(f"\nОтчет сохранен: {output_file}")

query = """SELECT
    COUNT(*) AS company_count,
    SUM(employees) AS total_employees,
    ROUND(AVG(employees), 2) AS avg_employees,
    MAX(employees) AS max_employees,
    MIN(employees) AS min_employees
FROM companies"""
result = con.execute(query).fetchdf()
print("\nОбщие показатели:")
print(result.to_string(index=False))

query = """SELECT
    city,
    COUNT(*) AS company_count,
    SUM(employees) AS total_employees,
    ROUND(AVG(employees), 2) AS avg_employees
FROM companies
GROUP BY city
ORDER BY total_employees DESC"""
result = con.execute(query).fetchdf()
print("\nАнализ по городам:")
print(result.to_string(index=False))

query = """SELECT
    industry,
    COUNT(*) AS company_count,
    SUM(employees) AS total_employees,
    ROUND(AVG(employees), 2) AS avg_employees
FROM companies
GROUP BY industry
ORDER BY total_employees DESC"""
result = con.execute(query).fetchdf()
print("\nАнализ по отраслям:")
print(result.to_string(index=False))

query = """SELECT
    city,
    COUNT(*) AS company_count,
    SUM(employees) AS total_employees
FROM companies
GROUP BY city
HAVING SUM(employees) >= 300
ORDER BY total_employees DESC"""
result = con.execute(query).fetchdf()
print("\nКрупные компании:")
print(result.to_string(index=False))

query = """SELECT
    city,
    COUNT(*) AS company_count
FROM companies
GROUP BY city
HAVING COUNT(*) >= 2
ORDER BY company_count DESC"""
result = con.execute(query).fetchdf()
print("\nНе менее двух организаций:")
print(result.to_string(index=False))

con.close()
