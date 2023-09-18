from flask import Flask
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import random
import datetime
import os
import sys

# df_user = pd.read_csv(r'./0905/USER_INFO_M.csv', encoding='gbk', index_col=0)
df_user = pd.read_csv(r'./0905/4/group4.csv', encoding='UTF-8')
print(df_user.columns)
print('---')
print(df_user.describe().T)
print('---')
print(df_user.isnull)
print('---')

print('---')
print(df_user.info())
print('---')
print(df_user.shape)
print('---')
print(df_user.head(3))
# df_user.to_csv(r'./0905/USER_INFO_OUTPUT.csv', encoding='UTF-8')


if __name__ == '__main__':
    print('---')


# /Users/ayu/PycharmProjects/chinaunicom_bigdata/0905/4