import socket
import time
from vgg16.model import Tudui,predict
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
from query import Database

set = ['Bread', 'Dairy product', 'Dessert', 'Egg', 'Fried food', 'Meat', 'Noodles/Pasta', 'Rice', 'Seafood', 'Soup', 'Vegetable/Fruit']
def server():
    # 创建 socket 对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    port = 3389
    # 绑定端口号
    server_socket.bind((host, port))
    # 设置最大连接数，超过后排队

    server_socket.listen(5)

    print('Server listening...')

    while True:
        # 建立客户端连接
        client_socket, addr = server_socket.accept()
        print("Got a connection from %s" % str(addr))

        localtime = time.asctime( time.localtime(time.time()))
        # 接收数据
        img_path = f'../Web/static/images/{localtime}.jpg'
        # print('进入with')
        with open(img_path, 'wb') as f:
            # print('进入while')
            while True:
                # print('开始接收')
                data = client_socket.recv(4086)
                if not data:
                    break
                f.write(data)

        print('Successfully got the file')   
        result = predict(img_path)
        
        time.sleep(1)
        client_socket.sendall(str(result).encode('utf-8'))
        
        print('预测结果发回客户端')
        time.sleep(1)
        client_socket.close()
        #数据库更新
        database = Database()
        result = str(result).encode('utf-8')
        result = result.decode('utf-8')
        print(result)
        database.add_food(name = set[int(result[-2])], food_class = int(result[-2]), image = img_path, QR = ' ')
        

server()

