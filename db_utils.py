import psycopg2


def get_conn():
    # 数据库连接参数
    db_params = {
        'dbname': 'database',
        'user': 'root',
        'password': 'Root',
        'host': '127.0.0.1',
        'port': '5432'
    }

    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    return conn, cursor
