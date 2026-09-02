import sqlite3, os
db_path = os.path.join(os.path.dirname(__file__),"etf_data.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT id,fund_code,fund_name FROM fund_brief LIMIT 5;")
print(cur.fetchall())
conn.close()
