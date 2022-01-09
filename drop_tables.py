import sqlite3

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()

c.execute("""SELECT COUNT(*) FROM sqlite_master WHERE type='table' 
                AND name in('county','host','review','stays','bookings')""")
if c.fetchone()[0] >= 1:
    c.execute("DROP TABLE stays")
    c.execute("DROP TABLE host")
    c.execute("DROP TABLE review")
    c.execute("DROP TABLE county")
    c.execute("DROP TABLE bookings")
else:
    pass

conn.commit()
c.close()
