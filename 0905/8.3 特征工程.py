# 代码 8-12
# 手机品牌独热编码
import pandas as pd
data_manu = pd.read_csv('../tmp/data_manu.csv', encoding='utf8')
data_manu.index = data_manu.iloc[:, 0]
data_manu = data_manu.drop(columns='USER_ID')

data_os = pd.read_csv('../tmp/data_os.csv', encoding='utf8')
data_os.index = data_os.iloc[:, 0]
data_os = data_os.drop(columns='USER_ID')

data_drop = pd.read_csv('../tmp/data_drop.csv', encoding='utf8')

data_group = pd.read_csv('../tmp/data_group.csv', encoding='utf8')
data_group.index = data_group.iloc[:, 0]
data_group = data_group.drop(columns='USER_ID')

data_agree = pd.read_csv('../tmp/data_agree.csv', encoding='utf8')
data_agree.index = data_agree.iloc[:, 0]
data_agree = data_agree.drop(columns='USER_ID')

data_credit = pd.read_csv('../tmp/data_credit.csv', encoding='utf8')
data_credit.index = data_credit.iloc[:, 0]
data_credit = data_credit.drop(columns='USER_ID')

data_vip = pd.read_csv('../tmp/data_vip.csv', encoding='utf8')
data_vip.index = data_vip.iloc[:, 0]
data_vip = data_vip.drop(columns='USER_ID')


data_manu = pd.get_dummies(data_manu)
print('独热编码后的手机品牌的形状：', data_manu.shape)
print(data_manu.head())
data_manu.to_csv('../tmp/data_manu.csv', encoding='utf8')

# 操作系统独热编码
data_os = pd.get_dummies(data_os)
print('独热编码后的操作系统的形状：', data_os.shape)
print(data_os.head())
data_os.to_csv('../tmp/data_os.csv', encoding='utf8')


# 代码 8-13
print('data_drop的形状：', data_drop.shape)
print(' data_group的形状：', data_group.shape)
print(' data_agree的形状：', data_agree.shape)
print(' data_vip的形状：', data_vip.shape)
print(' data_credit的形状：', data_credit.shape)
print(' data_manu的形状：', data_manu.shape)
print(' data_os的形状：', data_os.shape)

data_preprocessed = pd.concat([data_group, data_agree, data_vip, data_credit,
                               data_manu, data_os, ], axis=1)
print('合并后数据集的形状为:', data_preprocessed.shape)

data_preprocessed.columns = ['ACCT_FEE_median', 'ACCT_FEE_var',
                             'CALL_DURA_median', 'CALL_DURA_var',
                             'CDR_NUM_median', 'CDR_NUM_var',
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
                             'P2P_SMS_CNT_UP_median',
                             'P2P_SMS_CNT_UP_var',
                             'TOTAL_FLUX_median', 'TOTAL_FLUX_var',
                             'LOCAL_FLUX_median', 'LOCAL_FLUX_var',
                             'GN_ROAM_FLUX_median', 'GN_ROAM_FLUX_var',
                             'CALL_DAYS_median', 'CALL_DAYS_var',
                             'CALLING_DAYS_median', 'CALLING_DAYS_var',
                             'CALLED_DAYS_median', 'CALLED_DAYS_var',
                             'CALL_RING_median', 'CALL_RING_var',
                             'CALLING_RING_median', 'CALLING_RING_var',
                             'CALLED_RING_median', 'CALLED_RING_var',
                             'INNET_MONTH_median', 'INNET_MONTH_var',
                             'IS_AGREE', 'VIP_LVL', 'CREDIT_LEVEL',
                             'LG', '三星', '其他', '华为', '小米',
                             '联想', '苹果', '诺基亚',
                             '0_ANDROID', '0_BADA', '0_BB', '0_BLACKBERRY',
                             '0_IOS', '0_LINUX', '0_WINDOWS']
print(data_preprocessed.head())
data_preprocessed.to_csv('../tmp/data_preprocessed.csv', encoding='utf8')
