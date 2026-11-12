import duckdb
con = duckdb.connect()
query = """SELECT name, industry, city, employees
FROM read_csv_auto('data/raw/companies.csv')
ORDER BY employees DESC
LIMIT 3;"""
result = con.execute(query).fetchdf()
print(result.to_string(index=False))
con.close()
