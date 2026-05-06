from db import get_conn

conn = get_conn()
cur = conn.cursor()

cur.execute("SELECT 'FLASK CONNETCTED TO POSTGRES';")
print(cur.fetchone())

conn.close()