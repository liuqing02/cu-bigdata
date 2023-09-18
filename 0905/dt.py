import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import sklearn.ensemble as ensemble
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from collections import Counter
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier

from pymysql import *

conn = connect(host='127.0.0.1', user='root', password='root',
               database='cu-bigdata', charset='utf8')

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier


class CustomRandomForestClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, **kwargs):
        self.rfc = RandomForestClassifier(**kwargs)

    def fit(self, X, y):
        self.rfc.fit(X, y)

    def predict(self, X):
        return self.rfc.predict(X)


try:
    cur = conn.cursor()
    cur.execute(
        'select item_id, cat_id, merchant_id, brand_id, month, day, age_range, gender, CAST(province AS UNSIGNED) province, score, action from shopping_info;')

    columns = [col[0] for col in cur.description]

    data = []
    for i in cur.fetchall():
        data.append(i)

    df = pd.DataFrame(data, columns=columns)
    print('action: ', Counter(df['action']))

    y = df['action']
    X = df.iloc[:, :-1]

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2, random_state=10010)

    param_grid = {
        'criterion': ['entropy', 'gini'],
        'max_depth': range(10, 20, 1),  # 深度：这里是森林中每棵决策树的深度
        'n_estimators': [15,16,17],  # 决策树个数-随机森林特有参数
        'max_features': [0.8,0.9,1.0,1.1,1.2],  # 每棵决策树使用的变量占比-随机森林特有参数（结合原理）
        'min_samples_split': range(14, 28, 2)  # 叶子的最小拆分样本量
    }

    # rfc = ensemble.RandomForestClassifier(random_state=42)

    # 创建一个SimpleImputer对象，用均值填充缺失值
    imputer = SimpleImputer(strategy='mean')

    # 使用imputer来填充X_train和X_test中的缺失值
    X_train_imputed = imputer.fit_transform(X_train)
    X_test_imputed = imputer.transform(X_test)

    # rfc = CustomRandomForestClassifier(criterion='entropy', max_depth=5, n_estimators=11, max_features=0.3,
    #                                           min_samples_split=2, random_state=42)

    # rfc = ensemble.RandomForestClassifier(random_state=42)
    rfc = RandomForestClassifier(
        criterion='entropy',  # 设置你的参数
        max_depth=19,
        n_estimators=17,
        max_features=1.0,
        min_samples_split=14,
        random_state=42
    )

    rfc_cv = GridSearchCV(estimator=rfc, param_grid=param_grid,
                          scoring='accuracy', cv=5, n_jobs=-1)

    rfc.fit(X_train_imputed, y_train)
    rfc_cv.fit(X_train_imputed, y_train)
    test_est = rfc.predict(X_test_imputed)
    # ovr_classifier = OneVsRestClassifier(rfc)
    # ovr_classifier.fit(X_train_imputed, y_train)
    # 预测测试集
    # test_est = ovr_classifier.predict(X_test_imputed)

    print('随机森林分类报告...')
    print(classification_report(y_test, test_est, zero_division=1))  # 注意参数的顺序：真实标签在前，预测标签在后

    # 计算多类别 AUC
    y_probs = rfc.predict_proba(X_test_imputed)  # 使用 rfc 预测概率
    roc_auc = roc_auc_score(y_test, y_probs, average='macro', multi_class='ovr')  # 计算多类别 AUC
    print('多类别 AUC = %.4f' % roc_auc)

    print(rfc_cv.best_params_)

    # 预测测试集的标签概率
    y_probs = rfc_cv.predict_proba(X_test)

    # 将标签二值化为一个矩阵
    n_classes = 4
    y_test_bin = label_binarize(y_test, classes=range(n_classes))  # n_classes 为类别数量

    # 初始化字典来存储每个类别的 FPR 和 TPR
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    # 计算每个类别的 ROC 曲线
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_probs[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # 绘制多类别 ROC 曲线
    plt.figure(figsize=(10, 6))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    for i in range(n_classes):
        plt.plot(fpr[i], tpr[i], color=colors[i], lw=2,
                 label='ROC curve (class {0}) (area = {1:0.2f})'
                       ''.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=2)  # 画对角线
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Multi-Class ROC Curve')
    plt.legend(loc='lower right')
    plt.show()

except Exception as ex:
    print(ex)
finally:
    cur.close()
    conn.close()
