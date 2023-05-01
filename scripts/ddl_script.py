import mysql.connector
import re

conn = mysql.connector.connect(
    # host="localhost",
    host="db",
    user="root",
    password="password",
    database="pj5data"
)

cur = conn.cursor()

def exec_sql_file(cursor, sql_file):
    # print("\n[INFO] Executing SQL script file: '%s'" % (sql_file))
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):
            continue
        if not re.search(r';$', line):
            statement = statement + line
        else:  
            statement = statement + line
            # print("[DEBUG] Executing SQL statement:", statement)
            try:
                cursor.execute(statement)
            except Exception as e:
                print("[WARN] MySQLError during execute statement")
                print(e)

            statement = ""

exec_sql_file(cur, "ddl.sql")
conn.commit()
print("[DEBUG] Finished executing ddl_script.py statements")
cur.close()
conn.close()
