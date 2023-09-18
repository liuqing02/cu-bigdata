import pandas as pd
from tqdm import tqdm
import os

# 输入CSV文件路径
input_csv_file = "/Users/ayu/Downloads/UserBehavior.csv"
chunk_size = 5000000  # 每个CSV文件包含的行数

# 创建输出文件夹（如果不存在）
output_folder = "/Users/ayu/Downloads/ub"
os.makedirs(output_folder, exist_ok=True)

# 使用chunksize参数来逐块读取CSV文件
chunks = pd.read_csv(input_csv_file, chunksize=chunk_size)

# 计算总块数
total_chunks = sum(1 for _ in chunks)
chunks = pd.read_csv(input_csv_file, chunksize=chunk_size)  # 重新初始化chunks

# 逐块将数据保存为CSV文件
csv_file_prefix = "UserBehavior_chunk"
file_counter = 1

for chunk in tqdm(chunks, total=total_chunks, desc="Processing"):
    # 生成CSV文件名
    csv_file_name = os.path.join(output_folder, f"{csv_file_prefix}{file_counter}.csv")

    # 将数据保存为CSV文件
    chunk.to_csv(csv_file_name, index=False)

    file_counter += 1

print("CSV文件生成完成。")
