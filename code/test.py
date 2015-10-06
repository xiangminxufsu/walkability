from multiprocessing import Process, freeze_support
from sub import foo

if __name__ == '__main__':
    freeze_support()
    p = Process(target=foo)
    p.start()