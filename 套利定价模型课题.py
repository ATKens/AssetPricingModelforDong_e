import pandas as pd
import numpy as np
import statsmodels.api as sm

import warnings

# 禁用特定警告
warnings.filterwarnings("ignore", category=UserWarning, message="kurtosistest only valid for n>=20")

def process_yearly_data(file_path, date_column, value_column):
    """
    读取CSV文件，将日期转换为索引，按年份分组并取每年最后一个业务日的指定列值。

    :param file_path: CSV文件的路径
    :param date_column: 日期列的列名
    :param value_column: 感兴趣的值的列名
    :return: 按年份分组的数据的DataFrame
    """
    # 读取数据
    df = pd.read_csv(file_path)

    # 转换日期并设置为索引
    df[date_column] = pd.to_datetime(df[date_column])
    df.set_index(date_column, inplace=True)

    # 按年份分组，并取每年最后一个业务日的值
    yearly_values = df.resample('Y').last()

    # 返回感兴趣的列
    return yearly_values[value_column]

# 获取10年股价数据
file_path_stock_price = 'F:/套利定价模型课题/10年安琪酵母股价.csv'
yearly_close_prices = process_yearly_data(file_path_stock_price, 'Date', 'CloseFA')
yearly_close_prices = yearly_close_prices['2007':'2017'].values.tolist()
print("yearly_close_prices:",yearly_close_prices)

# 获取10年滚动扣非pe
file_path_koufeipettm = 'F:/套利定价模型课题/10年PE和PB.csv'
yearly_koufeipettm_value = process_yearly_data(file_path_koufeipettm, 'Date', 'koufei_pe_ttm')
yearly_koufeipettm_value = yearly_koufeipettm_value['2007':'2017'].values.tolist()
print("yearly_koufeipettm_value:",yearly_koufeipettm_value)

# 获取10年滚动pb
file_path_pb = 'F:/套利定价模型课题/10年PE和PB.csv'
yearly_pb_ttm_value = process_yearly_data(file_path_pb, 'Date', 'pb_ttm')
yearly_pb_ttm_value = yearly_pb_ttm_value['2007':'2017'].values.tolist()
print("yearly_pb_ttm_value:",yearly_pb_ttm_value)

# 获取动态股息率
file_path_dividend_yield = 'F:/套利定价模型课题/10年动态股息率.csv'
yearly_dividend_yield = process_yearly_data(file_path_dividend_yield, 'Date', 'dividend_yield')
yearly_dividend_yield = yearly_dividend_yield['2007':'2017'].values.tolist()
print("yearly_dividend_yield:",yearly_dividend_yield)

# 获取10年平均ROE
file_path_roe = 'F:/套利定价模型课题/10年平均ROE.csv'
yearly_roe = process_yearly_data(file_path_roe, 'Date', 'Roe')
yearly_roe = yearly_roe['2007':'2017'].values.tolist()
print("yearly_roe:",yearly_roe)

# 获取10年期国债收益率
file_path_Bond = 'F:/套利定价模型课题/10年期国债收益率.csv'
yearly_bond = process_yearly_data(file_path_Bond, 'Date', 'Bond_10year')
yearly_bond = yearly_bond['2007':'2017'].values.tolist()
yearly_bond = [float(value.strip('%'))/100 for value in yearly_bond]
print("yearly_bond:",yearly_bond)

# 获取10年市场贷款基准利率
file_path_lpr = 'F:/套利定价模型课题/10年市场贷款基准利率.csv'
yearly_lpr = process_yearly_data(file_path_lpr, 'Date', 'LPR')
yearly_lpr = yearly_lpr['2007':'2017'].values.tolist()
print("yearly_lpr:",yearly_lpr)

# 获取10年指数股息率
file_path_dividend_yield = 'F:/套利定价模型课题/10年指数股息率.csv'
yearly_dividend_yield = process_yearly_data(file_path_dividend_yield, 'Date', 'Dividend Yield')
yearly_dividend_yield = yearly_dividend_yield['2007':'2017'].values.tolist()
print("yearly_dividend_yield:",yearly_dividend_yield)


# 将列表合并为一个矩阵
data_matrix = np.column_stack([
    yearly_close_prices,
    yearly_koufeipettm_value,
    yearly_pb_ttm_value,
    yearly_dividend_yield,  # 可以选择使用第一组或第二组股息率数据
    yearly_roe,
    yearly_bond,
    yearly_lpr,
    yearly_dividend_yield
])
print("data_matrix_x加入截距前:",data_matrix)

y_values = data_matrix[:, 0]  # 第一列的值作为 Y
x_values = data_matrix[:, 1:] # 其他所有的值作为 X

# 在矩阵中加入截距
data_matrix = sm.add_constant(data_matrix)
print("data_matrix_x加入截距后:",data_matrix)

results = sm.OLS(y_values, x_values).fit()  # 进行回归并拟合模型
#print("results:",results)


"""给模型系数打分，去掉无统计显著性的"""

# 获取回归结果的系数
coefficients = results.params[0:]
print("coefficients:",coefficients)

# 获取回归结果的标准误差
std_err = results.bse
print("std_err:",std_err)

# 获取回归结果的t值
t_values = results.tvalues
print("t_values:",t_values)

# 获取P值
p_values = results.pvalues
print("p_values:",p_values)

# 获取回归结果的其他统计信息
summary = results.summary()
print("回归统计信息:\n", summary)
print("模型系数:",results.params)


# 构建模型评分的矩阵数据
model_scoring_matrix = np.column_stack([
    coefficients,
    std_err,
    t_values,
    p_values
])
print("model_scoring_matrix:\n",model_scoring_matrix)

model_scoring_matrix = model_scoring_matrix[model_scoring_matrix[:, 3] < 0.05]
print("model_scoring_matrix:\n",model_scoring_matrix)
"""说明市场基准贷款利率和10年期年收盘价这一个系数较合理"""