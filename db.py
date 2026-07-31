from psycopg2.pool import SimpleConnectionPool

pool = None

def init_db():
    global pool

    pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host="dpg-d9kf7om1egvs73eo2lpg-a.singapore-postgres.render.com",
        database="chquiz",
        user="chquiz_user",
        password="Pc82pYM8UtFIXrmdFXMGoDZrPorsAihN"
    )

def get_conn():
    return pool.getconn()

def release_conn(conn):
    pool.putconn(conn)