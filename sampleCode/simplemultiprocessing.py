from multiprocessing import Process
import os


def salute(course):
    print('Hello ', course)
    print('Parent process id:', os.getppid())
    print('Process id:', os.getpid())


if __name__ == '__main__':
    p = Process(target=salute, args=('DS',))
    p.start()
    p.join()
