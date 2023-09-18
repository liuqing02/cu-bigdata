import psycopg2
import csv
from tqdm import tqdm
from datetime import datetime, timedelta
import random
import io

# 定义行为类型映射字典
action_type_map = {
    'pv': 0,
    'buy': 1,
    'cart': 2,
    'fav': 3
}

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

# 循环导入多个CSV文件
for chunk_number in range(11, 20):
    # 构建CSV文件路径
    csv_file = f'/Users/ayu/Downloads/ub/UserBehavior_chunk{chunk_number}.csv'

    # 批次大小
    batch_size = 20000
    print(csv_file)
    # 打开CSV文件
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)

        data_to_insert = []
        inserted_count = 0

        for row in tqdm(csv_reader, desc=f"Inserting Data from Chunk {chunk_number}"):
            user_id, product_id, category_id, action_type, action_time = row

            # 处理action_time为空的情况
            if not action_time:
                start_date = datetime(2017, 11, 25)
                end_date = datetime(2017, 12, 3)
                random_time = start_date + timedelta(
                    seconds=random.randint(0, int((end_date - start_date).total_seconds())))
                action_time = datetime.fromtimestamp(random_time.timestamp())

            action_time = datetime.fromtimestamp(int(action_time))

            # 处理action_type为空的情况
            if not action_type:
                action_type = random.randint(0, 3)
            else:
                action_type = action_type_map.get(action_type, -1)

            # 处理user_id、product_id和category_id为空的情况
            if not user_id:
                user_id = 10010
            if not product_id:
                product_id = 10010
            if not category_id:
                category_id = 10010

            # 将数据添加到批次
            data_to_insert.append((user_id, product_id, category_id, action_type, action_time))
            inserted_count += 1

            # 如果批次达到指定大小，执行插入操作
            if inserted_count % batch_size == 0:
                virtual_file = io.StringIO()
                csv_writer = csv.writer(virtual_file)
                csv_writer.writerows(data_to_insert)
                virtual_file.seek(0)
                cursor.copy_expert(
                    "COPY user_behavior_partitioned (user_id, product_id, category_id, action_type, action_time) FROM stdin WITH CSV",
                    file=virtual_file
                )
                conn.commit()
                data_to_insert.clear()

        # 插入剩余的数据
        if data_to_insert:
            virtual_file = io.StringIO()
            csv_writer = csv.writer(virtual_file)
            csv_writer.writerows(data_to_insert)
            virtual_file.seek(0)
            cursor.copy_expert(
                "COPY user_behavior_partitioned (user_id, product_id, category_id, action_type, action_time) FROM stdin WITH CSV",
                file=virtual_file
            )
            conn.commit()

# 提交事务并关闭连接
cursor.close()
conn.close()

print("数据导入完成。")
