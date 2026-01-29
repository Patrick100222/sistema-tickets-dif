import sqlite3

conn = sqlite3.connect("ticket.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS tickets")

cursor.execute("""
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    area TEXT,
    problema TEXT,
    fecha TEXT,
    estado TEXT
)
""")

conn.commit()
conn.close()

print("Base de datos reiniciada correctamente")
