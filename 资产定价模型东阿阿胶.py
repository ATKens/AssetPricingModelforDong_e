import pandas as pd
from scipy.stats import linregress
import statistics

# 1. 导入CSV文件
df = pd.read_csv('F:/fundamental_sz000423.csv')  # 替换'your_file.csv'为实际的文件路径
df_sz = pd.read_csv('F:/szzs.csv')

# 2. 将日期列转换为日期时间类型
df['Date'] = pd.to_datetime(df['Date'])
df_sz['Date'] = pd.to_datetime(df_sz['Date'])

# 3. 将日期作为索引
df.set_index('Date', inplace=True)
df_sz.set_index('Date', inplace=True)

# 4. 按年度重采样
annual_data = df['Close'].resample('Y').last()
annual_sz_data = df_sz['Close'].resample('Y').last()

# 5. 计算年度收益率
annual_returns = annual_data.pct_change() * 100
annual_sz_returns = annual_sz_data.pct_change() * 100

print("--------------------东阿阿胶------------------\n")
print(annual_returns)
print("--------------------上证指数------------------\n")
print(annual_sz_returns)


#年度收益率转化为list并且取前10位，排除non位
stock_returns = annual_returns.tolist()
stock_returns_first_10_numbers = stock_returns[1:11]
print(stock_returns_first_10_numbers)

mkt_returns = annual_sz_returns.tolist()
mkt_returns_first_10_numbers = mkt_returns[8:18]
print(mkt_returns_first_10_numbers)

# 计算mkt总回报
total_returns = sum(mkt_returns_first_10_numbers)
print(total_returns)

# 观察期的年数
observation_period = len(mkt_returns_first_10_numbers)
print(observation_period)

# 计算平均回报率
average_returns = total_returns / observation_period
median_value = statistics.median(mkt_returns_first_10_numbers)
print("average_returns:",average_returns)
print("median_value:",median_value)

# 计算beta系数，这个系数就是指定stock的走势线相对于market的系数
beta,alpha,r_value,p_value,std_err = \
    linregress(stock_returns_first_10_numbers,mkt_returns_first_10_numbers)
print("beta               alpha")
print(beta,alpha)

"""
按中位数来看
ER = 3.5+0.47*(-1.79-3.5) 
ER = 1.0137%

按平均值来看
ER = 3.5+0.47*(3.155-3.5)
ER = 3.33785%

默认按平均回报率来算
说明当东阿阿胶当期年化收益>3.33785%的时候，此股被低估
当东阿阿胶当期年化收益<3.33785%的时候，此股被高估
"""
"""
stock_returns = [-58.029480, 95.378928, 97.256386, -15.419664, -5.160193,\
    -0.508221, -3.936298, 42.571160, 4.431768, 13.424370]
mkt_returns =[-65.394104, 79.982535, -14.313090, -21.675308, 3.169472,\
              -6.749283, 52.869120, 9.413605, -12.306240, 6.557784]
              
beta,alpha,r_value,p_value,std_err = \
    linregress(stock_returns,mkt_returns)
print("beta               alpha")
print(beta,alpha)
"""