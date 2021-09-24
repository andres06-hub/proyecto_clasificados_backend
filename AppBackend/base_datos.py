import pymysql

def crear_conexion():
    HOST = 'localhost'
    PORT = 3306
    USER = 'root'
    PASS = '0606'
    DB = 'clasificados_db'
    return pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        passwd=PASS,
        db=DB
    )

