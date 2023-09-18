from pymysql import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter


def get_df():
    conn = connect(host='123.56.89.159', user='root', password='root',
                   database='cu-bigdata', charset='utf8')
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
        return X_train, X_test, y_train, y_test
    except Exception as ex:
        print(ex)
    finally:
        cur.close()
        conn.close()
