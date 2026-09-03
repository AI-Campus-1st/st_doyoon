import pymysql
from pymysql.cursors import DictCursor

# BI 기본
def connect(db_config):
    return pymysql.connect(**db_config, 
                           cursorclass=DictCursor)

def select_order(conn:pymysql.Connect):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tb_order")
        result = cur.fetchall()
    return result
