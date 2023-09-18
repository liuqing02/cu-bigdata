# 初始化参数
w0 = 0
w1 = 0
alpha = 0.01  # 学习率
iterations = 1000  # 迭代次数

# 数据集
data = [(1.1, 1.9), (2.7, 2.3), (3.2, 3.4), (3.6, 2.9), (4.7, 3.4), (5.1, 4.3)]

# 梯度下降迭代
for _ in range(iterations):
    gradient_w0 = 0
    gradient_w1 = 0
    for x, y in data:
        y_pred = w0 + w1 * x
        gradient_w0 += (y_pred - y)
        gradient_w1 += (y_pred - y) * x
    gradient_w0 /= len(data)
    gradient_w1 /= len(data)

    # 更新参数
    w0 = w0 - alpha * gradient_w0
    w1 = w1 - alpha * gradient_w1

# 预测 x=6 时的 y(6)
x_new = 6
y_new = w0 + w1 * x_new

print("模型参数 w0:", w0)
print("模型参数 w1:", w1)
print("x=6 时的预测值 y(6):", y_new)
