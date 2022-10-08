from utils.helpers import *



if __name__ == '__main__':
    st = ts()
    print(f'thread: {tn()}')
    # print(f'task: {task_name()}')
    en = ts()
    print(f'elapsed: {en-st}s')