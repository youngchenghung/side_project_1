import pymysql

def connect_db():
    try:
        # 連線資料庫
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='11111111',
            port=3306
            )

        cursor = conn.cursor()
        print("Connected to the database")

        return conn, cursor
    
    except Exception as e:
        print("Error: ", e)
        

def close_db(conn, cursor):
    # 關閉資料庫連線
    cursor.close()
    conn.close()