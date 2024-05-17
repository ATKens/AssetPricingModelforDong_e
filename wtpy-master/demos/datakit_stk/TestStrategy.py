from wtpy import BaseCtaStrategy
from wtpy import CtaContext
import random
import pandas as pd

class MyStrategy(BaseCtaStrategy):
    def __init__(self, name: str, code: str, barCnt: int, period: str, days: int, k1: float, k2: float,
                 isForStk: bool = False):
        BaseCtaStrategy.__init__(self, name)

        self.__days__ = days
        self.__k1__ = k1
        self.__k2__ = k2

        self.__period__ = period
        self.__bar_cnt__ = barCnt
        self.__code__ = code

        self.__is_stk__ = isForStk

    def on_init(self, context: CtaContext):
        code = self.__code__  # 品种代码
        if self.__is_stk__:
            code = code + "-"  # 如果是股票代码，后面加上一个+/-，+表示后复权，-表示前复权
        print(f"---------------------------Initialized code: {code}")
        context.stra_prepare_bars(code, self.__period__, self.__bar_cnt__, isMain=True)  # 准备历史K线
        context.stra_sub_ticks(code)  # 订阅实时行情
        context.stra_log_text("DualThrust inited")

        # 读取存储的数据
        self.xxx = context.user_load_data('xxx', 1)
        #print("on_init----------------当前策略的股票代码列表:", self.codes)

    def on_calculate(self, context: CtaContext):
        # 在策略计算阶段也可以获取数据，例如，获取主要品种的额外数据
        #main_code = self.codes[0]  # 假设列表中的第一个股票为主要品种
        #context.stra_get_bars(stdCode=main_code, period='1d', count=20, isMain=True)
        # 进一步分析和交易逻辑...
        print("on_calculate----------------当前策略的股票代码列表:", self.codes)

    def calculate_dma_and_judge_market(df, column_name='close'):
        """
        计算DMA(15,30,10)并判断市场是强势还是弱势

        参数:
        df -- pandas DataFrame，包含股票数据
        column_name -- 字符串，DataFrame中收盘价列的名称，默认为'close'

        返回:
        布尔值，True表示强势市场，False表示弱势市场
        """
        # 确保column_name在df中
        if column_name not in df.columns:
            raise ValueError(f"列 {column_name} 不存在于DataFrame中")

        # 计算SMA15和SMA30
        df['SMA15'] = df[column_name].rolling(window=15).mean()
        df['SMA30'] = df[column_name].rolling(window=30).mean()

        # 计算DMA = SMA15 - SMA30
        df['DMA'] = df['SMA15'] - df['SMA30']

        # 对DMA值序列再应用一个10周期的SMA
        df['SMA_DMA'] = df['DMA'].rolling(window=10).mean()

        # 判断市场状态
        # 如果SMA_DMA的最新值大于0，则认为是强势市场
        if df['SMA_DMA'].iloc[-1] > 0:
            return True
        else:
            return False


