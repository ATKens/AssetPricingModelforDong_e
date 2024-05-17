import time
from wtpy import WtDtEngine,EngineType
from TestStrategy import MyStrategy

if __name__ == "__main__":
    # 创建一个运行环境，并加入策略
    env = WtDtEngine(EngineType.ET_SEL)
    env.initialize()
    env.add_cta_strategy(MyStrategy)
    env.run(True)

    print('press ctrl-c to exit')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt as e:
        exit(0)