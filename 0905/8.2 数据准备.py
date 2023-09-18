# 代码 8-1
import pandas as pd
# 读取数据文件
data = pd.read_csv('./0905/USER_INFO_M.csv', index_col=0, encoding='gbk')
data = data.iloc[1:1000,:]
print('原始数据形状为：', data.shape)

# 去除重复记录
data_drop = pd.DataFrame.drop_duplicates(data, subset=None, keep='first', inplace=False)
print('删除重复记录后的数据形状为：', data_drop.shape)


# 查找是否有重复特征
# 定义求取特征是否完全相同的矩阵的函数
def FeatureEquals(df):
    dfEquals = pd.DataFrame([], columns=df.columns, index=df.columns)
    for i in df.columns:
        for j in df.columns:
            dfEquals.loc[i, j] = df.loc[:, i].equals(df.loc[:, j])
    return dfEquals


detEquals = FeatureEquals(data_drop)  # 应用FeatureEquals函数
# 遍历所有数据
lenDet = detEquals.shape[0]
dupCol = []
for k in range(lenDet):
    for l in range(k+1, lenDet):
        if detEquals.iloc[k, l] & \
        (detEquals.columns[l] not in dupCol):
            dupCol.append(detEquals.columns[l])
# 删除重复列
data_drop.drop(dupCol, axis=1, inplace=True)
print('删除重复列后的数据形状：', data_drop.shape)



# 代码 8-2
# 数据降维
del data_drop['MODEL_NAME']  # 手机型号
del data_drop['AGREE_EXP_DATE']  # 删除合约是否到期
del data_drop['CUST_SEX']  # 性别
del data_drop['CONSTELLATION_DESC']  # 星座
del data_drop['CERT_AGE']  # 年龄
print('降维后的数据形状为:', data_drop.shape)



# 代码 8-3
# 统计各个特征的缺失率
naRate = (data_drop.isnull().sum()/
          data_drop.shape[0]*100).astype('str')+'%'
print('data每个特征缺失的率为：\n', naRate)



# 代码 8-4
# VIP等级为nan的补0
data_drop['VIP_LVL'] = data_drop['VIP_LVL'].fillna(0)
# 操作系统缺失的 填补ANDROID
data_drop['OS_DESC'] = data_drop['OS_DESC'].fillna('ANDROID')
print('处理缺失值后数据集的形状为：', data_drop.shape)



# 代码 8-5
# 对列统计分析
data_drop.describe()



# 代码 8-6
# 删除异常数据
data_drop = data_drop[data_drop['INNET_MONTH'] >= 0]
data_drop = data_drop[data_drop['ACCT_FEE'] < 400000]
print('处理异常值后数据集的形状为：', data_drop.shape)
data_drop.to_csv('../tmp/data_drop.csv', index=True, header='infer', encoding='utf8')



# 代码 8-7
import pandas as pd
import numpy as np

data_drop = pd.read_csv('../tmp/data_drop.csv', encoding='utf8')
data_group = data_drop.groupby("USER_ID").agg({
        'ACCT_FEE': [np.median, np.var],\
        'CALL_DURA': [np.median, np.var], 'CDR_NUM': [np.median, np.var],\
                  'NO_ROAM_LOCAL_CALL_DURA': [np.median, np.var],\
                  'NO_ROAM_LOCAL_CDR_NUM': [np.median, np.var],\
                  'NO_ROAM_GN_LONG_CALL_DURA': [np.median, np.var],\
                  'NO_ROAM_GN_LONG_CDR_NUM': [np.median, np.var],\
                  'GN_ROAM_CALL_DURA': [np.median, np.var], \
                  'GN_ROAM_CDR_NUM': [np.median, np.var], \
                  'NO_ROAM_CDR_NUM': [np.median, np.var],\
                  'P2P_SMS_CNT_UP': [np.median, np.var],
                  'TOTAL_FLUX': [np.median, np.var], \
                  'LOCAL_FLUX': [np.median, np.var], \
                  'GN_ROAM_FLUX': [np.median, np.var],\
                  'CALL_DAYS': [np.median, np.var], \
                  'CALLING_DAYS': [np.median, np.var],\
                  'CALLED_DAYS': [np.median, np.var],\
                  'CALL_RING': [np.median, np.var],\
                  'CALLING_RING': [np.median, np.var],\
                  'CALLED_RING': [np.median, np.var],\
                  'INNET_MONTH': [np.median, np.var], })

print('data_group的形状为:', data_group.shape)
data_group.columns = ['ACCT_FEE_median', 'ACCT_FEE_var', 'CALL_DURA_median', 
                      'CALL_DURA_var', 'CDR_NUM_median', 'CDR_NUM_var', 
                      'NO_ROAM_LOCAL_CALL_DURA_median', 
                      'NO_ROAM_LOCAL_CALL_DURA_var', 
                      'NO_ROAM_LOCAL_CDR_NUM_median', 
                      'NO_ROAM_LOCAL_CDR_NUM_var', 
                      'NO_ROAM_GN_LONG_CALL_DURA_median', 
                      'NO_ROAM_GN_LONG_CALL_DURA_var', 
                      'NO_ROAM_GN_LONG_CDR_NUM_median', 
                      'NO_ROAM_GN_LONG_CDR_NUM_var', 
                      'GN_ROAM_CALL_DURA_median', 
                      'GN_ROAM_CALL_DURA_var', 
                      'GN_ROAM_CDR_NUM_median', 
                      'GN_ROAM_CDR_NUM_var', 
                      'NO_ROAM_CDR_NUM_median', 
                      'NO_ROAM_CDR_NUM_var', 
                      'P2P_SMS_CNT_UP_median', 'P2P_SMS_CNT_UP_var', 
                      'TOTAL_FLUX_median', 'TOTAL_FLUX_var', 
                      'LOCAL_FLUX_median', 'LOCAL_FLUX_var', 
                      'GN_ROAM_FLUX_median', 'GN_ROAM_FLUX_var', 
                      'CALL_DAYS_median', 'CALL_DAYS_var', 
                      'CALLING_DAYS_median', 'CALLING_DAYS_var', 
                      'CALLED_DAYS_median', 'CALLED_DAYS_var', 
                      'CALL_RING_median', 'CALL_RING_var', 
                      'CALLING_RING_median', 'CALLING_RING_var', 
                      'CALLED_RING_median', 'CALLED_RING_var', 
                      'INNET_MONTH_median', 'INNET_MONTH_var']

data_group.to_csv('../tmp/data_group.csv', index=True, header='infer', encoding='utf8')



# 代码 8-8
# 将每个用户三个月的合约是否有效，合并为一条记录
# 定义合并合约有效记录函数
def fun1(data):
    if data.shape[0] != 3:
        return 0
    elif sum(data.iloc[:, 1] == 1) == 3:
        return 1.5
    else:
        return data.iloc[-1, 1] - data.iloc[:2, 1].mean()


data_agree = data_drop[["USER_ID",
                        "IS_AGREE"]].groupby("USER_ID").apply(lambda x: fun1(x))
print('data_agree的形状为:', data_agree.shape)
print(data_agree.head())
data_agree.to_csv('../tmp/data_agree.csv', index=True, header='infer', encoding='utf8')



# 代码 8-9
# 将每个用户三个月的VIP等级合并为一条记录
def fun2(data):
    if data.shape[0] != 3:
        return 0
    elif(data.iloc[0, 1] == data.iloc[1, 1]) & (data.iloc[0, 1] == data.iloc[2, 1]):
        return data.iloc[2, 1]
    else:
        return data.iloc[2, 1] - data.iloc[:2, 1].mean()


data_vip = data_drop[['USER_ID',
                      'VIP_LVL']].groupby('USER_ID').apply(lambda x: fun2(x))
print('data_vip的形状为:', data_vip.shape)
print(data_vip.head())
data_vip.to_csv('../tmp/data_vip.csv', index=True, header='infer', encoding='utf8')



# 代码 8-10
# 取每个用户三个月信用等级的平均数作为一行记录
data_credit = data_drop.groupby('USER_ID').agg({'CREDIT_LEVEL': np.mean, })
data_credit.iloc[:10]
print('data_credit的形状为:', data_credit.shape)
print(data_credit.head())
data_credit.to_csv('../tmp/data_credit.csv', index=True, header='infer', encoding='utf8')



# 代码 8-11
# 简化手机品牌
string = ['苹果', '小米', '华为', '三星', '诺基亚', '联想', 'LG']


def Replace(x=None, string=string):
    if x not in string:
        x = '其他'
    return x


# 每个ID的手机品牌只取第一个月的
data_str = data_drop.groupby("USER_ID").apply(lambda x: x.iloc[0])
data_manu = data_str['MANU_NAME'].apply(Replace)
print('data_manu的形状为:', data_manu.shape)
print(data_manu.head())

# 简化操作系统
# 每个ID的手机操作系统也只取第一个月的
data_id = data_drop.groupby("USER_ID").apply(lambda x: x.iloc[0])
data_os = data_id["OS_DESC"].str.extract("([A-Z]+)")  # 保留所有的字母
print('data_os的形状为:', data_os.shape)
print(data_os.head())
data_manu.to_csv('../tmp/data_manu.csv', index=True, header='infer', encoding='utf8')
data_os.to_csv('../tmp/data_os.csv', index=True, header='infer', encoding='utf8')

