#!/usr/bin/env python

'''
聊天客户端

1. 建立与服务器的连接
2. 建立接收线程：收到消息后自动打印
3. 建立发送线程：等待用户数据, 用户输入完后，将消息发送到服务器
4. 用户输入 'exit' 后，将消息发到服务器，然后关闭连接，最后退出客户端
'''
import sys
import socket
import threading


class RecvThread(threading.Thread):
    '''消息接收线程'''

    def __init__(self, sock):
        super().__init__()
        self.daemon = True
        self.sock = sock

    def run(self):
        while True:
            msg = self.sock.recv(1024)
            print(msg.decode('utf-8'))


def main(host, port):
    addr = (host, port)
    sock = socket.socket()
    sock.connect(addr)  # 与服务器建立连接

    # 创建并启动消息接收线程
    recv_thread = RecvThread(sock)
    recv_thread.start()

    # 等待用户输入消息，并发送
    while True:
        msg = input('请输入: ')
        msg = msg.encode('utf-8')
        sock.send(msg)

        if msg == b'exit':
            sock.close()
            break


if __name__ == "__main__":
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except (IndexError, TypeError):
        print('请输入正确的参数')

    main(host, port)
