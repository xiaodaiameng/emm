from concurrent.futures import ThreadPoolExecutor

def fn(name):
    for i in range(19):
        print(name,i)

if __name__ == '__main__':
    # 创建线程池
    with ThreadingPoolExecutor(20) as t:
        for i in range(50):
            t.submit(fn, name=f"线程{i}")
    # 线程池任务全部执行完毕，才继续执行后面的内容（一种守护方式）
    print("123")