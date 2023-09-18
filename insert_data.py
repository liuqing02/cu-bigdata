import csv
import psycopg2
from datetime import datetime
from tqdm import tqdm

# 定义行为类型映射字典
action_type_map = {
    'pv': 0,
    'buy': 1,
    'cart': 2,
    'fav': 3
}

# 输入CSV文件路径
csv_file = '/Users/ayu/Downloads/ub/UserBehavior_chunk1.csv'

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

# 打开CSV文件并插入数据
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    data_to_insert = []
    batch_size = 1000
    for row in tqdm(csv_reader, desc="Inserting Data"):
        user_id, product_id, category_id, action_type, timestamp = row
        action_type = action_type_map.get(action_type, -1)  # 获取行为类型映射
        datetime_obj = datetime.fromtimestamp(int(timestamp))
        data_to_insert.append((int(user_id), int(product_id), int(category_id), action_type, datetime_obj))

        if len(data_to_insert) == batch_size:
            # 插入数据到表中
            cursor.executemany(
                "INSERT INTO user_behavior_partitioned (user_id, product_id, category_id, action_type, action_time) VALUES (%s, %s, %s, %s, %s)",
                data_to_insert
            )
            conn.commit()
            data_to_insert.clear()

    # 插入剩余的数据（少于1000条）
    if data_to_insert:
        cursor.executemany(
            "INSERT INTO user_behavior (user_id, product_id, category_id, action_type, datetime) VALUES (%s, %s, %s, %s, %s)",
            data_to_insert
        )
        conn.commit()

# 关闭连接
cursor.close()
conn.close()

print("数据插入完成。")
