import sqlite3
conn = sqlite3.connect("obd_data.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM obd_codes")
print(cursor.fetchall())
conn.close()