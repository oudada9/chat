#!/usr/bin/env python

'''
聊天室服务器

1. 建立 Server Socket 对象，等待客户端连接
2. 接收客户端连接，并保存到连接池
3. 建立客户端线程，等待接受消息
4. 接收到消息后，转发给其他所有客户端
5. 收到 'exit' 数据后，关闭客户端连接，将连接对象从连接池删除
'''

import socket
import threading


class ClientThread(threading.Thread):
    def __init__(self, sock, addr, conn_pool, pool_lock):
        super().__init__()
        self.daemon = True
        self.sock = sock
        self.addr = addr
        self.conn_pool = conn_pool
        self.pool_lock = pool_lock

    def broadcast(self, msg):
        '''广播'''
        for addr, sock in self.conn_pool.items():
            if addr != self.addr:  # 排除自己
                sock.send(msg)  # 给其他人发消息

    def exit(self):
        '''退出'''
        self.sock.close()
        with self.pool_lock:
            self.conn_pool.pop(self.addr)

    def run(self):
        '''线程的主函数'''
        while True:
            msg = self.sock.recv(1024)
            if msg in [b'exit', b'']:
                self.exit()
            else:
                self.broadcast(msg)
            break


def main():
    '''主程序'''
    addr = ('0.0.0.0', 8000)  # 服务器地址
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(1024)
    print('服务器开始监听: %s:%s' % addr)

    # 连接池对象
    conn_pool = {}
    pool_lock = threading.Lock()

    while True:
        cli_sock, cli_addr = sock.accept()
        print('收到客户端连接: %s:%s' % addr)
        with pool_lock:
            conn_pool[cli_addr] = cli_sock  # 将 cli_sock 放入连接池
        cli_thread = ClientThread(cli_sock, cli_addr, conn_pool, pool_lock)
        cli_thread.start()
        cli_thread.join()



if __name__ == "__main__":
    main()
