import pandas as pd
from datetime import datetime, timedelta
import random
import os

# 定义行为类型映射字典
action_type_map = {
    'pv': 0,
    'buy': 1,
    'cart': 2,
    'fav': 3
}

# CSV文件路径
csv_file = '/Users/ayu/Downloads/ub/UserBehavior_chunk20.csv'
save_file_path = '/Users/ayu/Downloads/ub/virtual_file/20.csv'

# 读取CSV文件为DataFrame
df = pd.read_csv(csv_file, header=None, names=['user_id', 'product_id', 'category_id', 'action_type', 'action_time'])

# 批量写入的数据大小
batch_size = 5000
data_to_insert = []

# 处理数据并批量写入
for index, row in df.iterrows():
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
    if pd.isna(action_type):
        action_type = random.randint(0, 3)
    else:
        action_type = action_type_map.get(action_type, -1)

    # 处理user_id、product_id和category_id为空的情况
    if pd.isna(user_id):
        user_id = 10010
    if pd.isna(product_id):
        product_id = 10010
    if pd.isna(category_id):
        category_id = 10010

    # 将数据添加到批次
    data_to_insert.append((user_id, product_id, category_id, action_type, action_time))

    # 如果累积了足够多的数据，批量写入到磁盘
    if len(data_to_insert) >= batch_size:
        virtual_file = pd.DataFrame(data_to_insert, columns=['user_id', 'product_id', 'category_id', 'action_type', 'action_time'])
        virtual_file.to_csv(save_file_path, mode='a', header=False, index=False)
        data_to_insert = []

# 写入剩余的数据
if data_to_insert:
    virtual_file = pd.DataFrame(data_to_insert, columns=['user_id', 'product_id', 'category_id', 'action_type', 'action_time'])
    virtual_file.to_csv(save_file_path, mode='a', header=False, index=False)

print("数据导入完成。")
