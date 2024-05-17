"""

筛选条件:
主板或创业板，总市值<50亿 ，peg<10，市净率>1&<2，市盈率小于40，5日的区间涨跌幅<1%，不包含st ，按市盈率从小到大
强弱市场是通过DMA(15,30,10)区分
强势市场：止盈 : 收益率 ≥ 10 % 时坚定持有;直到最高收益回落 6%,止损 : 收益率 ≤ - 5 %
弱势市场:止盈 : 收益率 ≥ 7 % 时坚定持有;直到最高收益回落 3 %止损 : 收益率 ≤ - 3 %

"""
import akshare as ak
import pandas as pd
import time


# 获取A股股票列表
def get_astocklist():
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    return stock_zh_a_spot_df

def filter_main_stock(stock_zh_a_spot_df):
    # 筛选主板股票
    # 上海主板以"600", "601"或"603"开头，深圳主板以"000"开头
    main_board_stocks = stock_zh_a_spot_df[
        stock_zh_a_spot_df["代码"].str.startswith(("sh600", "sh601", "sh603", "sz000"))
    ]

    # 筛选创业板股票
    # 创业板股票代码以"300"开头
    gem_board_stocks = stock_zh_a_spot_df[
        stock_zh_a_spot_df["代码"].str.startswith("sz300")
    ]
    """
    # 输出主板股票列表
    print("主板股票列表:")
    print(main_board_stocks)

    # 输出创业板股票列表
    print("创业板股票列表:")
    print(gem_board_stocks)
    """
    combined_stocks = pd.concat([main_board_stocks, gem_board_stocks])
    return combined_stocks

# 获取指定股票代码的市值
def get_market_cap(stock_code):
    stock_code = stock_code[2:]
    stock_info = ak.stock_individual_info_em(symbol=stock_code)
    market_cap = stock_info.loc[stock_info['item'] == '总市值', 'value'].iloc[0]
    return market_cap

# 接收股票代码DataFrame，返回市值DataFrame
def get_market_caps_dataframe(stock_codes_df):
    # 初始化市值列表
    market_caps_list = []

    # 遍历DataFrame中的股票代码
    for code in stock_codes_df.iloc[:, 0]:  # 假设股票代码在第一列
        time.sleep(0.001)
        # 获取市值
        market_cap = get_market_cap(code)
        # 将市值添加到列表中
        market_caps_list.append(market_cap)

    # 将市值列表转换为DataFrame
    market_caps_df = pd.DataFrame(market_caps_list, columns=['Market Cap'])

    return market_caps_df

# 获取筛选后的第一列数据
def get_first_column_from_second_row(df):
    # 提取第一列从第二行到末尾的数据
    first_column_data = df.iloc[0:, 0].to_frame()
    return first_column_data

# 转换stock_code,获取的st_stock_code的总的stock_code格式不同
def convert_stock_code(code):
    if len(code) == 6 and code[0] in ['3', '0']:
        return 'sz' + code
    elif len(code) == 6:
        return 'sh' + code
    else:
        return code

def get_non_st_astocks(all_astocks):
    # 获取st股票
    st_stocks = ak.stock_zh_a_st_em()
    # 转换ST股票代码格式与A股列表一致
    st_stock_codes = st_stocks['代码'].apply(convert_stock_code).tolist()
    # 从A股列表中排除ST股
    non_st_astocks = all_astocks[~all_astocks['代码'].isin(st_stock_codes)]

    return non_st_astocks

if __name__ == '__main__':
    print("数据计算中，请稍等......\n")
    # 获取所有股票数据
    #stock_zh_a_spot_df = get_astocklist()

    stock_zh_a_spot_df = pd.read_csv('F:/pythonProject/filter_main_stock_list.csv')#Debug

    # 获取所有主板或创业板股票数据
    filter_main_stock_list = filter_main_stock(stock_zh_a_spot_df)

    # 给filter_main_stock_list添加核心数据列
    first_column_data = get_first_column_from_second_row(filter_main_stock_list)
    market_caps_dataframe = get_market_caps_dataframe(first_column_data)

    # 水平合并
    horizontal_merged_df = pd.concat([stock_zh_a_spot_df, market_caps_dataframe], axis=1)
    horizontal_merged_df.to_csv('horizontal_merged_df.csv', encoding='utf_8_sig', index=False)


"""
#non_st_astocks.to_csv('non_st_astocks.csv',encoding='utf_8_sig', index=False)
    df = first_column_data.iloc[0,0]
    print("df:\n",df)
    market = get_market_cap(df)
    print("market:\n",market)
    """

"""
    df = pd.read_csv('F:/pythonProject/first_column_data.csv')
    value = df.iloc[1599, 0]
    print(value)
"""