import asyncio
import time


async def func1():
    print("helloTask111.")
    # time.sleep(2) 不能加同步操作，否则异步会中断，不产生异步效果
    await asyncio.sleep(2) # 要睡觉上一边睡去，不要让其他程序等，要求协程找没有睡觉的程序继续干活
    print("helloTask111.")

async def func2():
    print("helloTask222.")
    # time.sleep(2)
    await asyncio.sleep(2)
    print("helloTask222.")

async def func3():
    print("helloTask333.")
    # time.sleep(2)
    await asyncio.sleep(2)
    print("helloTask333.")


if __name__ == '__main__':

    f1 = func1()
    f2 = func2()
    f3 = func3()
    # print(f1)会是什么？

    tasks = [f1,f2,f3]

    t1 = time.time()

    asyncio.run(asyncio.wait(tasks))

    t2 = time.time()

