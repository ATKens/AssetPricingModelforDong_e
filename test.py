import akshare as ak
import pandas as pd
from datetime import datetime, timedelta



def get_stock_code_30day_price_close_df(stock_code):
    # 获取当前日期
    current_date = datetime.now().date()

    # 转换为 'YYYYMMDD' 格式的字符串
    current_time_str = current_date.strftime('%Y%m%d')

    # 获取100天前的日期
    date_days_ago = current_date - timedelta(days=100)

    # 转换为 'YYYYMMDD' 格式的字符串
    date_days_ago_str = date_days_ago.strftime('%Y%m%d')

    stock_zh_a_cdr_daily_df = ak.stock_zh_a_cdr_daily(symbol=stock_code, \
                                                      start_date=date_days_ago_str, end_date=current_time_str)
    #print(stock_zh_a_cdr_daily_df)
    last_45_rows_close = stock_zh_a_cdr_daily_df.iloc[-45:]['close']

    return last_45_rows_close.to_frame()


# Ture 强势、False 弱势
def is_strong_weak_market(df):
    # 计算15日和30日SMA
    df['SMA_15'] = df['close'].rolling(window=15).mean()#15
    df['SMA_30'] = df['close'].rolling(window=30).mean()#30

    # 计算DMA
    df['DMA'] = df['SMA_15'] - df['SMA_30']

    # 计算DMA的10日SMA
    df['DMA_SMA10'] = df['DMA'].rolling(window=10).mean()
    """
    # 显示最后几行数据作为结果示例
    print(df.tail())
    print("df['DMA'].iloc[-1]\n",df['DMA'].iloc[-1])
    print("df['DMA_SMA10'].iloc[-1]\n",df['DMA_SMA10'].iloc[-1])
    """
    return df['DMA'].iloc[-1] > df['DMA_SMA10'].iloc[-1]


def trade_decision(df):
    # 假设df有一列'return'表示每天的收益率（例如，0.1表示10%）
    max_return_so_far = 0
    for i, daily_return in enumerate(df['return']):
        # 检查止损条件
        if daily_return <= -0.05:
            return f"Stop loss triggered on day {i + 1}"

        # 更新目前为止的最大收益率
        if daily_return > max_return_so_far:
            max_return_so_far = daily_return

        # 检查止盈条件
        if max_return_so_far >= 0.1 and (max_return_so_far - daily_return) >= 0.06:
            return f"Take profit triggered on day {i + 1}"

    return "Hold"


if __name__ == '__main__':
    last_45_rows_close = get_stock_code_30day_price_close_df('sh600004')
    #print(last_45_rows_close)
    ret_boolean = is_strong_weak_market(last_45_rows_close)
    print(ret_boolean)
