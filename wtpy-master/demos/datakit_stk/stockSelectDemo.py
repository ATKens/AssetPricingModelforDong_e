from wtpy import BaseCtaStrategy
from wtpy import CtaContext
import random
import pandas as pd


class StraHushenStk(BaseCtaStrategy):
    def __init__(self, name: str, codes: list, capital: float, barCnt: int, period: str):
        BaseCtaStrategy.__init__(self, name)

        self.__capital__ = capital  # 起始资金
        self.__period__ = period  # 交易k线的时间级，如5分钟，1天
        self.__bar_cnt__ = barCnt  # 拉取的bar的次数
        self.__codes__ = codes  # 所有沪深300成分股股票代码
        self.__codes2__ = []  # 每日50股票池

    def on_init(self, context: CtaContext):
        codes = self.__codes__  # 所有沪深300成分股股票代码
        codes2 = self.__codes2__  # 每日50股票池

        for i in range(0, len(codes)):
            if i == 0:
                context.stra_get_bars(codes[i], self.__period__, self.__bar_cnt__, isMain=True)  # 设置第一支股票为主要品种
            else:
                context.stra_get_bars(codes[i], self.__period__, self.__bar_cnt__, isMain=False)

        context.stra_log_text("Hushen inited")

    def on_calculate(self, context: CtaContext):
        codes = self.__codes__  # 所有沪深300成分股股票代码
        codes2 = self.__codes2__  # 每日50股票池
        capital = self.__capital__  # 初始资金
        date = context.stra_get_date()  # 获取当前日期

        # 读取当日对应的沪深300成分股代码
        stocks = pd.read_csv('E:/沪深300历年成分股/{}.csv'.format(date), index_col=0)['order_book_id'].values

        nums = []  # 股票池的数量
        while len(nums) < 50:  # 每日固定生成50个不重复的随机数
            num = random.randint(0, len(stocks) - 1)
            if num in nums:  # 若随机数重复，跳过
                pass
            elif num not in nums:  # 确保保存的随机数不重复
                stock = stocks[num]
                if stock[-1] == 'E':  # 将深市股票代码转化为wtpy识别的股票代码
                    code = "SZSE.STK.{}".format(stock[:6])
                    curPrice = context.stra_get_price(code)
                    if curPrice > 0:  # 确保股票当日价格数据正常
                        codes2.append(code)  # 将股票放入股票池
                        nums.append(num)  # 将随机数放入nums
                elif stock[-1] == 'G':  # 将沪市股票代码转化为wtpy识别的股票代码
                    code = "SSE.STK.{}".format(stock[:6])
                    curPrice = context.stra_get_price(code)
                    if curPrice > 0:  # 确保股票当日价格数据正常
                        codes2.append(code)  # 将股票放入股票池
                        nums.append(num)  # 将随机数放入nums

        for code in list(context.stra_get_all_position().keys()):  # 遍历当前的持仓
            curPos = context.stra_get_position(code)  # 获取每只股票的持仓头寸
            if code not in codes2 and curPos > 0:  # 若当前持有的股票不在新生成的股票池内
                context.stra_exit_long(code, curPos, 'exitlong')  # 平仓

        for code in codes2:  # 遍历股票池
            curPos = context.stra_get_position(code)  # 获取当前仓位
            curPrice = context.stra_get_price(code)  # 获取当前价格
            if curPos == 0:  # 若尚未持仓，买入该股票
                unit = int((200000 / curPrice) / 100)  # 确定买入的数量
                context.stra_enter_long(code, unit, 'enterlong')  # 买入unit手code
            elif curPos > 0:  # 若已经持有该股票，则继续保留
                pass
        self.__codes2__ = []  # 当天交易结束后，将股票池清空
