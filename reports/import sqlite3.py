import sqlite3

conn = sqlite3.connect("2_IPL_Cricket/ipl.db")
cursor = conn.cursor()

print("===== DELIVERIES =====")
cursor.execute("PRAGMA table_info(deliveries);")

for column in cursor.fetchall():
    print(column)

print("\n===== MATCHES =====")
cursor.execute("PRAGMA table_info(matches);")

for column in cursor.fetchall():
    print(column)
