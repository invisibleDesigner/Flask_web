import time


def count(ipt):
    return len(ipt)


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def last_active_time(unix_timestamp):
    li = ['几秒前', '几分钟前', '几小时前', '几天前']

    now = time.time()
    diff_time = int(now - unix_timestamp)

    if diff_time <= 60:
        return li[0]
    elif diff_time <= 3600:
        return li[1]
    elif diff_time <= 24*3600:
        return li[2]
    else:
        return li[3]


def log(*args, **kwargs):
    fmt = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    with open('log/web.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, **kwargs, file=f)
