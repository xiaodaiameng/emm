进程是资源单位，
线程是执行单位


多线程：
from threading import Thread

def func1():
    for i in range(0, 11):
        print("func1: helloWorld.", i)

def func2():
    for i in range(0, 11):
        print("func2: helloWorld.", i)

if __name__ == '__main__':
    t1 = Thread(target=func1)
    t1.start() # 表示提示你多线程状态为可以开始工作的状态，具体执行时间由 cpu 决定

    t2 = Thread(target=func2)
    t2.start()

    for i in range(0,11):
        print("Main: helloWorld.",i) # 程序运行，发现并发了，结果就是混着打印


# 以上是直接写方法，也可以写类，
# class MyThread(Thread):
#     def run(self):固定run？
#         for i in range(0, 11):
#             print("class's func: helloWorld.", i)
#
# if __name__ == '__main__':
#     t = MyThread()
#     t.run()????????????
#     t.start()

# 还可以传递参数：
# def func1(name):
#     for i in range(0, 11):
#         print(f"func1: {name}", i)
#
# if __name__ == '__main__':
#     t1 = Thread(target=func1, args=("周杰伦",))# 必须是元祖
#     t1.start()
