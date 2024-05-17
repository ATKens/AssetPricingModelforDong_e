from wtpy import WtEngine, EngineType
from TestStrategy import MyStrategy
import time

if __name__ == "__main__":
    # 创建一个运行环境，并加入策略
    engine = WtEngine(EngineType.ET_SEL)
    engine.init('../common/', "config.yaml", commfile="stk_comms.json", contractfile="stocks.json")

    myStrategy = MyStrategy(name='pydt_SH600000', code="SSE.STK.600000", barCnt=50,\
                            period="d1", days=30, k1=0.1, k2=0.1, isForStk=True)
    engine.add_cta_strategy(myStrategy)

    engine.run(True)
    print('press ctrl-c to exit')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt as e:
        exit(0)
