import logging
import queue
import threading

import skyland
import push

# 华为云本地文件在./code下面
file_save_token = './code/INPUT_HYPERGRYPH_TOKEN.txt'

logging.getLogger().setLevel(logging.INFO)


def read(path):
    v = []
    with open(path, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            i = i.strip()
            i and i not in v and v.append(i)
    return v


def handler():
    token = read(file_save_token)
    if token:
        all_logs = []
        result_queue = queue.Queue()
        threads = []
        for i in range(0, len(token)):
            t = threading.Thread(target=start, args=(token[i], result_queue))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        while not result_queue.empty():
            all_logs.extend(result_queue.get())
        push.push(all_logs)


def start(token, result_queue):
    try:
        cred = skyland.get_cred_by_token(token)
        success, logs_out = skyland.do_sign(cred)
        result_queue.put(logs_out)
    except Exception as ex:
        err = f'签到失败，原因：{str(ex)}'
        logging.error(err, exc_info=ex)
        result_queue.put([err])


handler()
