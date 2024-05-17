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
import datetime
import concurrent.futures

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
    # 获取所有ST股列表
    st_stocks = ak.stock_zh_a_st_em()

    # 转换ST股票代码格式与A股列表一致
    st_stock_codes = st_stocks['代码'].apply(convert_stock_code).tolist()

    # 从A股列表中排除ST股
    non_st_astocks = all_astocks[~all_astocks['代码'].isin(st_stock_codes)]

    return non_st_astocks

# 水平合并
def horizontal_merge(df1,df2):
    # 在合并前重置索引
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    # 确保两个 DataFrame 的行数相同
    assert len(df1) == len(df2), "DataFrames do not have the same number of rows."

    # 水平合并
    horizontal_merged_df = pd.concat([df1, df2], axis=1)
    return horizontal_merged_df

# 输入stock_code矩阵，返回对应的市盈率矩阵
def get_latest_pe_values(stock_codes_df,indicator,period,columns_name):
    # 初始化存储市盈率的列表
    pe_values = []

    # 遍历股票代码
    for code in stock_codes_df.iloc[:, 0]:
        time.sleep(0.001)
        try:
            # 获取每个股票的市盈率（TTM）数据
            pe_df = ak.stock_zh_valuation_baidu(symbol=code[2:], indicator=indicator, period=period)
            # 获取最后一行的市盈率值
            latest_pe = pe_df['value'].iloc[-1]
            pe_values.append(latest_pe)
        except Exception as e:
            print(f"get_latest_pe_values:Error occurred for stock code {code}: {e}")
            pe_values.append(None)

    # 将市盈率值转换为DataFrame
    pe_values_df = pd.DataFrame(pe_values, columns=[columns_name])

    return pe_values_df

# 5日的区间涨跌幅
def get_5day_price_range(stock_code):
    # 获取当前日期
    current_date_root = current_date = datetime.date.today()

    current_date = current_date.strftime('%Y%m%d')
    #print("current_date:", current_date)

    five_days_ago = current_date_root - datetime.timedelta(days=20)

    five_days_ago = five_days_ago.strftime('%Y%m%d')
    #print("five_days_ago:", type(five_days_ago))

    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=five_days_ago,
                                            end_date=current_date, adjust="")
    #stock_zh_a_hist_df.to_csv('stock_zh_a_hist_df.csv', encoding='utf_8_sig', index=False)

    current_day_close_price = stock_zh_a_hist_df.iloc[-1, 2]
    five_days_ago_close_price = stock_zh_a_hist_df.iloc[-5, 2]
    #print(current_day_close_price)
    #print(five_days_ago_close_price)

    ret_value_5day_range = (current_day_close_price-five_days_ago_close_price)/five_days_ago_close_price
    return ret_value_5day_range

# 输入stock_code矩阵，返回对应的5日的区间涨跌幅矩阵
def calculate_price_ranges(stock_codes,columns_name):
    # 初始化一个空的列表来存储变动值
    price_ranges = []

    # 遍历股票代码列表
    for code in stock_codes.iloc[:, 0]:
        time.sleep(0.001)
        # 对每个股票代码调用之前定义的函数
        try:
            price_range = get_5day_price_range(code[2:])
            price_ranges.append(price_range)
        except Exception as e:
            # 如果在获取数据时发生错误，记录错误信息
            print(f"calculate_price_ranges:Error getting data for stock code {code}: {e}")
            price_ranges.append(None)  # 使用None或合适的值来表示错误

    pe_values_df = pd.DataFrame(price_ranges, columns=[columns_name])
    return pe_values_df

# 计算peg
def get_stock_code_eps(stock_code):
    try:
        stock_current_period_eps_root = ak.stock_financial_abstract_ths(symbol=stock_code, indicator="按年度")
        stock_current_period_eps = float(stock_current_period_eps_root.iloc[0, 7])  # 当期每股收益
        stock_last_period_eps = float(stock_current_period_eps_root.iloc[1, 7])

        # 检查分母是否为零
        if stock_last_period_eps == 0:
            # 处理分母为零的情况
            return None  # 或者选择其他合适的值或方法来处理这种情况
        else:
            eps_year = (stock_current_period_eps - stock_last_period_eps) / stock_last_period_eps
            return eps_year
    except Exception as e:
        # 处理其他可能的错误
        print(f"get_stock_code_peg:Error getting data for stock code {stock_code}: {e}")
        return None

def calculate_eps_df(stock_codes,columns_name):
    # 初始化一个空的列表来存储变动值
    peg_year_ranges = []

    # 遍历股票代码列表
    for code in stock_codes.iloc[:, 0]:
        time.sleep(0.001)
        try:
            peg_year = get_stock_code_eps(code[2:])
            peg_year_ranges.append(peg_year)
        except Exception as e:
            # 如果在获取数据时发生错误，记录错误信息
            print(f"calculate_eps_df:Error getting data for stock code {code}: {e}")
            peg_year_ranges.append(None)  # 使用None或合适的值来表示错误

    pe_values_df = pd.DataFrame(peg_year_ranges, columns=[columns_name])
    return pe_values_df

"""
根据函数个数，函数参数，自动创建线程

用法：
tasks = [
        (work_function_1, [1]),
        (work_function_2, [1, 2]),
        (work_function_3, [1, 2, 3])
    ]
    results = main(tasks)

    # 获取并使用work_function_2的返回值
    df_result = results["work_function_3"]
    print("Result from work_function_2:\n", df_result)

"""
def main(tasks):
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = {executor.submit(func, *args): func.__name__ for func, args in tasks}

        # 等待所有线程完成
        for future in concurrent.futures.as_completed(futures):
            func_name = futures[future]
            results[func_name] = future.result()

        print("All threads are done. Executing the main thread.")
    return results


# 获取peg
def calculate_peg(pe_df, eps_growth_df, pe_column, eps_growth_column):
    """
    计算PEG比率。

    :param pe_df: 包含市盈率数据的DataFrame。
    :param eps_growth_df: 包含每股收益增长率数据的DataFrame。
    :param pe_column: 市盈率数据所在的列名。
    :param eps_growth_column: 每股收益增长率数据所在的列名。
    :return: 包含PEG比率的DataFrame。
    """
    # 确保两个DataFrame有相同的行索引
    if len(pe_df) == len(eps_growth_df):
        # 计算PEG比率
        peg_values = pe_df[pe_column] / eps_growth_df[eps_growth_column]
        return pd.DataFrame({ 'PEG': peg_values })
    else:
        print("DataFrames do not have the same length.")
        return None

if __name__ == '__main__':

    print("数据矩阵构建中，可能需要较长时间，请稍等......\n")
    # 获取所有股票数据
    stock_zh_a_spot_df = get_astocklist()
    stock_zh_a_spot_df.to_csv('stock_zh_a_spot_df.csv', encoding='utf_8_sig', index=False)

    # stock_zh_a_spot_df = pd.read_csv('F:/pythonProject/stock_zh_a_spot_df.csv')#Debug

    # 剔除掉st的
    stock_zh_a_spot_df = get_non_st_astocks(stock_zh_a_spot_df)

    # 获取所有主板或创业板股票数据
    filter_main_stock_list = filter_main_stock(stock_zh_a_spot_df)

    
    # 给filter_main_stock_list添加核心数据列
    

    # 获取第一列stock_code矩阵
    first_column_data = get_first_column_from_second_row(filter_main_stock_list)

    # 获取市值矩阵
    market_caps_dataframe = get_market_caps_dataframe(first_column_data)

    # 重置索引的水平合并
    horizontal_merged_df = horizontal_merge(filter_main_stock_list,market_caps_dataframe)

    # 输入stock_code矩阵，返回对应的市盈率矩阵
    latest_pe_values_df = get_latest_pe_values(first_column_data,"市盈率(TTM)","近一年",'市盈率')
    #latest_pe_values_df.to_csv('latest_pe_values_df.csv', encoding='utf_8_sig', index=False)



    # 输入stock_code矩阵，返回对应的市净率矩阵
    latest_pb_values_df = get_latest_pe_values(first_column_data, "市净率", "近一年",'PB')

    # 重置索引水平合并pettm和pb
    latest_pe_pb_df = horizontal_merge(latest_pe_values_df,latest_pb_values_df)

    # 重置索引水平合并pe_pb_df和all_df
    horizontal_merged_df = horizontal_merge(horizontal_merged_df,latest_pe_pb_df)

    # 获取5日的区间涨跌幅矩阵
    df_5day_price_range = calculate_price_ranges(first_column_data,'5日的区间涨跌幅')

    # 获取eps矩阵
    eps_df = calculate_eps_df(first_column_data, 'eps')

    # 获取peg矩阵
    peg_df = calculate_peg(latest_pe_values_df, eps_df, '市盈率', 'eps')

    #将peg矩阵和5日的区间涨跌幅矩阵合并
    df_5day_price_range_and_peg_df =  horizontal_merge(df_5day_price_range, peg_df)
    #df_5day_price_range_and_peg_df.to_csv('df_5day_price_range_and_peg_df.csv', encoding='utf_8_sig', index=False)

    #将合并后的矩阵再和all_df合并
    horizontal_merged_df = horizontal_merge(horizontal_merged_df, df_5day_price_range_and_peg_df)
    horizontal_merged_df.to_csv('horizontal_merged_df.csv', encoding='utf_8_sig', index=False)

    # 按照规则筛选

    full_criteria = (
            (horizontal_merged_df["Market Cap"] < 50E9) &
            (horizontal_merged_df["PEG"] < 10) &
            (horizontal_merged_df["PB"] > 1) & (horizontal_merged_df["PB"] < 2) &
            (horizontal_merged_df["市盈率"] > 0) & (horizontal_merged_df["市盈率"] < 40) &
            (horizontal_merged_df["5日的区间涨跌幅"] < 0.01)
    )

    filtered_stocks_full_criteria = horizontal_merged_df[full_criteria]
    filtered_stocks_full_criteria = filtered_stocks_full_criteria.sort_values(by="市盈率")#按pe从小到大排列
    filtered_stocks_full_criteria.to_csv('filtered_stocks_full_criteria.csv', encoding='utf_8_sig', index=False)

    """
    horizontal_merged_df.to_csv('horizontal_merged_df.csv', encoding='utf_8_sig', index=False)
    """

