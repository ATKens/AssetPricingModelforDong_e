from scipy.optimize import brentq
from scipy.stats import norm
import numpy as np

# 实现布莱克-斯克尔斯看涨期权定价公式
def black_scholes_call(S, K, r, q, T, sigma):
    # 计算d1和d2参数
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # 根据d1和d2计算看涨期权的理论价格
    call_price = (S * np.exp(-q * T) * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    return call_price

# 实现计算隐含波动率的函数
def implied_volatility(C_market, S, K, r, q, T):
    # 定义目标函数：市场价格与理论价格的差异
    def objective(sigma):
        return black_scholes_call(S, K, r, q, T, sigma) - C_market
    # 使用brentq方法求解使目标函数为零的波动率
    return brentq(objective, 0.0001, 2.0)

# 设置示例参数
S = 2.562  # 标的资产当前价格（上证50 ETF）
K = 2.6    # 行权价格
r = 0.0231 # 年化无风险利率（以小数形式）
q = 0.01621 # 年化股息率（以小数形式）
T = 0.126   # 期权到期时间（以年为单位）
C_market = 0.0248  # 已知的看涨期权市场价格

# 计算隐含波动率
implied_vol = implied_volatility(C_market, S, K, r, q, T)
print("看涨期权的隐含波动率:",implied_vol)
