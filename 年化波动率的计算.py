import numpy as np

# 上证50指数的收盘价数据
prices = np.array([2.512, 2.5242, 2.5592, 2.568, 2.5602])

# 计算对数收益率
log_returns = np.log(prices[1:] / prices[:-1])

# 计算日收益率的标准差
daily_std = np.std(log_returns, ddof=1)

# 计算年化波动率
annual_volatility = daily_std * np.sqrt(252)

print("年化波动率为:", annual_volatility)