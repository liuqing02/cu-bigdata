import sys

# 获取当前 Python 解释器的虚拟环境根目录
virtualenv_root = sys.prefix

print("Virtualenv Root Directory:", virtualenv_root)

print("------")
interpreter_path = sys.executable

print("Virtualenv Interpreter Path:", interpreter_path)

for chunk_number in range(11, 20):
    print(chunk_number)