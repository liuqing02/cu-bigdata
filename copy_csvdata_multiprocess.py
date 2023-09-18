import psycopg2
import csv
import datetime
import random
import io
import logging
from multiprocessing import Pool
from tqdm import tqdm  # 导入tqdm

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

# 日志设置
logging.basicConfig(filename='data_import.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 处理单行数据的函数
def process_row(row):
    user_id, product_id, category_id, action_type, action_time = row

    # 处理日期时间
    if not action_time:
        start_date = datetime.datetime(2017, 11, 25)
        end_date = datetime.datetime(2017, 12, 3)
        random_time = start_date + datetime.timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        action_time = random_time
    else:
        action_time = datetime.datetime.fromtimestamp(int(action_time))

    # 处理动作类型
    action_type = action_type_map.get(action_type, -1)

    # 处理为空的字段
    if not user_id:
        user_id = 10010
    if not product_id:
        product_id = 10010
    if not category_id:
        category_id = 10010

    return user_id, product_id, category_id, action_type, action_time

try:
    # 连接到 PostgreSQL 数据库
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # CSV 文件路径
    # 5 6 done 21 20
    csv_file = '/Users/ayu/Downloads/ub/UserBehavior_chunk7.csv'

    # 批次大小
    batch_size = 30000

    # 打开 CSV 文件
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        data_to_insert = []

        # 获取总行数以用于进度条
        total_rows = sum(1 for _ in csv_reader)
        file.seek(0)  # 重新定位文件指针

        # 使用tqdm创建进度条
        progress_bar = tqdm(total=total_rows, desc="Inserting Data")

        # 多进程处理
        with Pool() as pool:
            for row in csv_reader:
                processed_row = pool.apply(process_row, (row,))
                data_to_insert.append(processed_row)

                # 如果批次达到指定大小，执行插入操作
                if len(data_to_insert) >= batch_size:
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

                # 更新进度条
                progress_bar.update(1)

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

        # 关闭进度条
        progress_bar.close()

    # 提交事务并关闭连接
    cursor.close()
    conn.close()
    logging.info("数据导入完成。")

except Exception as e:
    logging.error(f"数据导入过程中发生错误: {str(e)}")
