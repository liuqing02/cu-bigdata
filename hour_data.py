import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import db_utils
from matplotlib.font_manager import FontProperties


# 连接到 PostgreSQL 数据库
conn, cursor = db_utils.get_conn()

# 执行 SQL 查询并将结果存储在 Pandas DataFrame 中
sql_query = """
SELECT EXTRACT(HOUR FROM action_time) AS hour_range,
       COUNT(action_type) AS "总点击次数",
       SUM(CASE WHEN action_type = 0 THEN 1 ELSE 0 END) AS "点击次数",
       SUM(CASE WHEN action_type = 1 THEN 1 ELSE 0 END) AS "收藏次数",
       SUM(CASE WHEN action_type = 2 THEN 1 ELSE 0 END) AS "加购数",
       SUM(CASE WHEN action_type = 3 THEN 1 ELSE 0 END) AS "购买次数"
FROM user_behavior_partitioned
GROUP BY hour_range
ORDER BY hour_range;
"""


font = FontProperties(fname=r'/Users/ayu/Library/Fonts/字体文件-宋体_常规.ttc')

df = pd.read_sql_query(sql_query, conn)

# 关闭数据库连接
conn.close()

# 使用 Matplotlib 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(df['hour_range'], df['总点击次数'], label='总点击次数', marker='o', linestyle='-')
plt.plot(df['hour_range'], df['点击次数'], label='点击次数', marker='o', linestyle='-')
plt.plot(df['hour_range'], df['收藏次数'], label='收藏次数', marker='o', linestyle='-')
plt.plot(df['hour_range'], df['加购数'], label='加购数', marker='o', linestyle='-')
plt.plot(df['hour_range'], df['购买次数'], label='购买次数', marker='o', linestyle='-')

plt.title('Hourly Action Counts')
plt.xlabel('Hour of the Day')
plt.ylabel('Count')
plt.grid(True)
plt.legend(prop=font)
plt.yticks(range(0, max(df['总点击次数']) + 1, 300000))
plt.show()
