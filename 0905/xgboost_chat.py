import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score
import xgboost as xgb
from xgboost import XGBClassifier, plot_importance
import warnings
import data_utils

warnings.filterwarnings('ignore')
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

X_train, X_test, y_train, y_test = data_utils.get_df()

num_classes = 4

def xgboost_parameters():
    params = {'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'min_child_weight': [1, 2, 3, 4, 5, 6]}
    fine_params = {'n_estimators': 50}
    return params, fine_params


def model_adjust_parameters(cv_params, other_params):
    model = XGBClassifier(**other_params, objective='multi:softmax', num_class=num_classes)
    optimized_param = GridSearchCV(estimator=model, param_grid=cv_params, scoring='accuracy', cv=5, verbose=2)
    optimized_param.fit(X_train, y_train)
    means = optimized_param.cv_results_['mean_test_score']
    params = optimized_param.cv_results_['params']
    for mean, param in zip(means, params):
        print("mean_score: %f,  params: %r" % (mean, param))
    print('参数的最佳取值：{0}'.format(optimized_param.best_params_))
    print('最佳模型得分:{0}'.format(optimized_param.best_score_))

    parameters_score = pd.DataFrame(params, means)
    parameters_score['means_score'] = parameters_score.index
    parameters_score = parameters_score.reset_index(drop=True)
    parameters_score.to_excel('parameters_score.xlsx', index=False)

    plt.figure(figsize=(15, 12))
    plt.subplot(2, 1, 1)
    plt.plot(parameters_score.iloc[:, :-1], 'o-')
    plt.legend(parameters_score.columns.to_list()[:-1], loc='upper left')
    plt.title('Parameters_size', loc='left', fontsize='xx-large', fontweight='heavy')
    plt.subplot(2, 1, 2)
    plt.plot(parameters_score.iloc[:, -1], 'r+-')
    plt.legend(parameters_score.columns.to_list()[-1:], loc='upper left')
    plt.title('Score', loc='left', fontsize='xx-large', fontweight='heavy')
    plt.show()


if __name__ == '__main__':
    adj_params, fixed_params = xgboost_parameters()
    model_adjust_parameters(adj_params, fixed_params)
