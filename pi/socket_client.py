import socket

def client(name):
    # 创建 socket 对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = '39.106.32.166'
    port = 3389
    # 连接服务，指定主机和端口
    client_socket.connect((host, port))

    # 打开图片文件
    with open(name, 'rb') as f:
        # 按块读取文件内容并发送
        while True:
            data = f.read(1024)
            if not data:
                break
            client_socket.sendall(data)

    print('Successfully sent the file')
    client_socket.shutdown(socket.SHUT_WR)
    response = client_socket.recv(1024)  # 可根据需要调整接收的数据大小
    result = response.decode('utf-8')
    set = ['Bread', 'Dairy product', 'Dessert', 'Egg', 'Fried food', 'Meat', 'Noodles/Pasta', 'Rice', 'Seafood', 'Soup', 'Vegetable/Fruit']
    print('Received from server:', result , '食物分类为', set[int(result[-2])])

    client_socket.close()

if __name__ == '__main__':
    client(name = './cat.jpg')
