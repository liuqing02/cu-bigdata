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


# boston = datasets.load_boston()


server = Flask(__name__, static_folder='')
@server.route('/')
def index():
    return 'hello world'


def model_test():
    iris = datasets.load_iris()
    x_iris_train, x_iris_test, y_iris_train, y_iris_test = train_test_split(iris.data, iris.target, test_size=0.2,
                                                                            random_state=100)
    model_dt = DecisionTreeClassifier()
    model_dt.fit(x_iris_train, y_iris_train)
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    joblib.dump(model_dt, r'./0904/model/dt_model_' + date + '.pkl')
    # model = joblib.load(r'./0904/model/dt_model.pkl')
    result_1 = model_dt.predict(x_iris_test)
    print(result_1)
    print(y_iris_test)
    print(accuracy_score(y_iris_test, result_1))


if __name__ == '__main__':
    model_test()

    # print(iris.target[119])
    # print(iris.target_names[iris.target[119]])
    # print(boston.data.shape)
    # server.run(host='0.0.0.0', port=8081)
