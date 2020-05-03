#! /usr/bin python3
# -*- coding: utf-8 -*-


from collections import namedtuple
import queue
import random
import argparse
import time


# 定义几个常量
DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5


Event = namedtuple('Event', ('time', 'proc', 'action'))


def taxi_process(ident, trips, start_time=0):
    """每次改变状态时创建事件（Event），把控制权让给仿真器"""
    time = yield Event(start_time, ident, "leave garage")
    for i in range(trips):
        time = yield Event(time, ident, "pick up passenger")
        time = yield Event(time, ident, "drop off passenger")
    yield Event(time, ident, "going home")


def compute_duration(previous_action):
    """使用指数分布计算操作耗时"""
    if previous_action in ("leave garage", "drop off passenger"):
        # 新状态是四处徘徊
        interval = SEARCH_DURATION
    elif previous_action == "pick up passenger":
        # 新状态是形成开始
        interval = TRIP_DURATION
    elif previous_action == "going home":
        interval = 1
    else:
        raise ValueError("Unknown previous_action: %s" % previous_action)
    return int(random.expovariate(1/interval)) + 1


class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()  # 一个evnet容器，存储上次产出event
        self.procs = dict(procs_map)  # 出租车进程的协程对象映射副本

    def run(self, end_time):
        """调度并显示事件，知道事件结束"""

        # 调度个车辆出租车的第一个事件
        for _, proc in sorted(self.procs.items()):  # 应该没必要排序在此
            first_event = next(proc)  # 激活协程并得到第一个事件
            self.events.put(first_event)

        # 此次仿真的主循环
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():  # 只留存上一次event，所以仿真完毕队列为空
                print("""*** end of events ***""")
                break
            # 从队列中获取上次事件
            current_event = self.events.get()

            # 具名元组解包
            sim_time, proc_id, previous_action = current_event
            print("taxi:", proc_id, proc_id * ' ', current_event)
            
            # 从协程映射中获取当前协程对象
            active_proc = self.procs[proc_id]

            # 根据状态获取离散模拟时间
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)

        else:
            msg = "*** end of simulation time: {} events pending ***"
            print(msg.format(self.events.qsize()))


# 定义主函数
def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS, seed=None):
    if seed is not None:
        random.seed(seed)
    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL) for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Taxi fleet simulator.")
    parser.add_argument('-e', '--end-time', type=int, default=DEFAULT_END_TIME,
                        help="simulation end time; default=%s" % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int, default=DEFAULT_NUMBER_OF_TAXIS,
                        help="number of taxis running; default=%s" % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help="random generator seed (for testing)")
    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)
    