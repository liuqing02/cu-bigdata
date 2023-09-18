# 代码 8-14
#导入库
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

# 导入数据
data_drop = pd.read_csv('../tmp/data_drop.csv', encoding='utf-8', index_col=0)
data_preprocessed = pd.read_csv('../tmp/data_preprocessed.csv', 
                                encoding='utf-8', index_col=0)
# 取data_preprocessed作为输入，取data_drop中三月份的数据的目标变量作为输出
data_target = data_drop.loc[:, ['USER_ID', 'IS_LOST']]
data_target = data_target.loc[data_target["USER_ID"].isin(data_preprocessed.index)]
data_target = data_target.loc[201603].drop_duplicates()
print('目标变量数据集的形状为:', data_target.shape)
# 划分数据集
x = data_preprocessed
y = data_target
x_train, x_test, y_train, y_test = train_test_split(x, y['IS_LOST'], test_size=0.2,
                                                    random_state=42)
print('训练集数据的形状为：', x_train.shape)
print('训练集标签的形状为：', y_train.shape)
print('测试集数据的形状为：', x_test.shape)
print('测试集标签的形状为：', y_test.shape)
# 数据标准化
stdScaler = StandardScaler().fit(x_train)
x_stdtrain = stdScaler.transform(x_train)
x_stdtest = stdScaler.transform(x_test)
print('标准化后的x_stdtrain:\n', x_stdtrain)
print('标准化后的x_stdtest:\n', x_stdtest)



# 代码 8-15
# 建立模型
bpnn = MLPClassifier(hidden_layer_sizes=(17, 10),\
                     max_iter=200, solver='lbfgs', random_state=50)
bpnn.fit(x_stdtrain, y_train)
print('构建的模型为:\n', bpnn)



# 代码 8-16
# 模型预测
y_pre = bpnn.predict(x_stdtest)
print('多层感知器预测结果评价报告：\n', classification_report(y_test, y_pre))

# %matplotlib inline
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

# 绘制ROC曲线图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
fpr, tpr, thresholds = roc_curve(y_pre, y_test)  # 求出TPR和FPR
plt.figure(figsize=(6, 4))  # 创建画布
plt.plot(fpr, tpr)  # 绘制曲线
plt.title('用户流失模型的ROC曲线')  # 标题
plt.xlabel('FPR')  # x轴标签
plt.ylabel('TPR')  # y轴标签
plt.show()  # 显示图形
plt.close
