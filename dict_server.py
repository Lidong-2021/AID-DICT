from socket import *
from multiprocessing import Process
import signal
import sys
from mysql import *
from time import sleep

# 定义全局变量
HOST = '0.0.0.0'
POST = 8000
ADDR = (HOST, POST)
# 建立数据库连接
db = Database(database='dict')


# 注册
def do_register(c, data):
    tem = data.split(' ')
    name = tem[1]
    passwd = tem[2]
    # 如果返回Ture表示注册成功，False表示失败
    if db.register(name, passwd):
        c.send(b"ok")
    else:
        c.send(b'fail')


# 登录
def do_sign_in(c, data):
    tem = data.split(' ')
    name = tem[1]
    passwd = tem[2]
    if db.do_sign_in(name, passwd):
        c.send(b"ok")
    else:
        c.send(b'fail')


def do_hist(c, data):
    tem = data.split(' ')
    name = tem[1]
    r = db.do_hist(name)
    if r:
        c.send(b'ok')
        sleep(0.01)
        for i in r:
            msg = '%-16s %s' % i
            c.send(msg.encode())
            sleep(0.01)
        c.send(b'##')
    else:
        c.send(b'fail')


# 查询单词
def do_query(c, data):
    tem = data.split(' ')
    name = tem[1]
    word = tem[2]
    r = db.query(name, word)
    c.send(r.encode())


# 请求处理
def request(c):
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ":", data)
        if not data or data == '':
            c.close()
            break
        elif data[0] == 'R':
            do_register(c, data)
        elif data[0] == 'Q':
            do_query(c, data)
        elif data[0] == 'S':
            do_sign_in(c, data)
        elif data[0] == 'H':
            do_hist(c, data)


# 建立链接
def mian():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print('listen the port 8000')
    while True:
        try:
            c, addr = s.accept()
            print('connect from', addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit('服务端退出')
        except Exception as e:
            print(e)
            continue
        # 为客户端创建子进程
        p = Process(target=request, args=(c,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    mian()
