"""
dict 客户端
"""
from socket import *
import sys

s = socket()
server_addr = ('127.0.0.1', 8000)
s.connect(server_addr)


# 查询
def query(s, name):
    word = input('word:')
    request = 'Q %s %s' % (name, word)
    s.send(request.encode())
    data = s.recv(1024).decode()
    print(data)


# 历史记录
def hist(name):
    request = "H %s" % name
    s.send(request.encode())
    data = s.recv(1024).decode()
    print(data)


# 进入二级界面
def login(name):
    while True:
        print("""
        ======================================
        1.查单词        2.历史记录        3.注销
        ======================================
        """)
        cmd = input("请输入指令")
        if cmd == '1':
            query(s, name)
        elif cmd == '2':
            hist(name)
        elif cmd == '3':
            return
        else:
            print('请输入正确指令')


# 注册
def register(s):
    while True:
        name = input("请输入用户名：")
        if ' ' in name:
            print('用户名不能有空格')
            continue
        while True:
            password = input("请输入密码：")
            if " " in password:
                print('密码不能有空格')
                continue
            break
        request = 'R %s %s' % (name, password)
        s.send(request.encode())
        data = s.recv(1024).decode()
        if data == 'ok':
            print('注册成功')
            login(name)
            break
        else:
            print('注册失败')
            break

# 登录
def sign_in(s):
    while True:
        name = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        request = 'S %s %s' % (name, password)
        s.send(request.encode())
        data = s.recv(1024).decode()
        if data == 'ok':
            print('登录成功')
            login(name)
            break
        else:
            print('登录失败，用户名或密码错误')


def main():
    while True:
        print("""
        =========================
        1.注册    2.登录    3.退出
        =========================
        """)
        # 发送消息
        cmd = input('Msg>>')
        if cmd == '1':
            register(s)
        elif cmd == '2':
            sign_in(s)
        elif cmd == '3':
            sys.exit('谢谢使用')
        else:
            print('请输入正确的指令')


if __name__ == '__main__':
    main()
