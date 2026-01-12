import sqlite3
import json

conn = sqlite3.connect('instance/yojanamitra.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT id, name, benefits, eligibility, application_process, documents_required FROM scheme WHERE name LIKE "%Netaji Subhas%"')
rows = cursor.fetchall()

result = []
for r in rows:
    result.append(dict(r))

with open('db_inspect_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"Found {len(result)} schemes. Results saved to db_inspect_result.json")
conn.close()
