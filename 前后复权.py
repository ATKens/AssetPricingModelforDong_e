import numpy as np
import pandas as pd

# 设置随机种子以便复现结果
np.random.seed(0)

# 生成30天的模拟收盘价格数据
dates = pd.date_range(start="2024-01-01", periods=30, freq='D')
close_prices = np.random.normal(loc=100, scale=10, size=len(dates))  # 假设平均价格100，标准差10

# 创建DataFrame
stock_data = pd.DataFrame(data={'Close': close_prices}, index=dates)

# 假设第15天发生了2:1的股票分拆
split_date = stock_data.index[14]
split_ratio = 2

# 前复权
stock_data['Adj Close (前复权)'] = stock_data['Close'].copy()
stock_data.loc[:split_date, 'Adj Close (前复权)'] /= split_ratio

# 后复权
stock_data['Adj Close (后复权)'] = stock_data['Close'].copy()
stock_data.loc[split_date:, 'Adj Close (后复权)'] *= split_ratio

stock_data20 = stock_data.head(20)  # 显示前20天的数据进行检查
print(stock_data20)