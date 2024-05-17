import pandas as pd
import threading
import time

running = True
# 重新定义函数
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




def get_user_input():
    while running:
        # 获取用户输入
        user_input = input("请输入一系列以逗号分隔的每日仓位权益值,正常情况一天输入一次: ")

        # 将输入的字符串拆分成列表
        input_list = user_input.split(',')

        # 将列表中的每个字符串转换为浮点数
        try:
            return_list = [float(item) for item in input_list]
        except ValueError:
            print("输入错误，逗号用英文逗号,确保您输入的是数字，并用逗号分隔。")
            return_list = []

        # 将转换后的列表赋值给data字典
        data = {
            'return': return_list
        }

        # 打印结果以验证
        print(data)
        if len(return_list) < 2:
            print("数据池数据少于2条，请添加。")

        # 计算每天收益率变化的百分比
        percent_changes = [(data['return'][i] - data['return'][i - 1]) / data['return'][i - 1] for i in
                           range(1, len(data['return']))]

        # 创建新的数据字典
        data = {
            'return': percent_changes
        }
        df_example = pd.DataFrame(data)
        print("源数据:\n", df_example)
        # 应用交易决策函数
        decision = trade_decision(df_example)
        print(decision)
        time.sleep(1)

if __name__ == '__main__':
    # 创建线程
    thread = threading.Thread(target=get_user_input)

    # 启动线程
    thread.start()

    # 等待线程完成
    thread.join()

    print("线程结束")




