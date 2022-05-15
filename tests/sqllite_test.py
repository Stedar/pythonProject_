import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

con = sqlite3.connect('q_table.db')
#con.row_factory = dict_factory
cursor = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS states
               (col0 real,col1 real, col2 real,col3 real,col4 real, col5 real, col6 real, id text PRIMARY KEY)''')
cursor.execute("INSERT INTO q_table VALUES (-0.25,0,0,-0.25,0,0,0,'h2') ON CONFLICT(id) DO UPDATE SET col0=excluded.col0,col1=excluded.col1,col2=excluded.col2,col3=excluded.col3,col4=excluded.col4,col5=excluded.col5,col6=excluded.col6; ")

# Save (commit) the changes
con.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

sqlite_select_query = """SELECT * from states"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()

q_table = {}

for i in records:
    q_table[i[8]] = i[:8]


con.close()



#
# con = sqlite3.connect(":memory:")
# con.row_factory = dict_factory
# cur = con.cursor()
# cur.execute("select 1 as a")
# print cur.fetchone()["a"]