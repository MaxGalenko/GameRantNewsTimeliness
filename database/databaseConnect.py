from datetime import datetime
from databaseFunctions import *

cur.execute("select * from information_schema.tables where table_name=%s", ('mytable',))
if cur.rowcount == 0:
    createTables()
