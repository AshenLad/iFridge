from rich.console import Console
from rich.table import Table
from query import Database
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import cv2
from scanQR import scan
from socket_client import client
from AdafruitDHT import cond
import time
from QR import QR


ASYNC_CACHE = []#缓存区

def hello_console():
    
    console.clear()
    console.print("[bold red]Hello[/bold red]")

    table = Table(title="智能冰箱控制界面")

    table.add_column("按键", justify="center", style="cyan", no_wrap=True)
    table.add_column("功能", style="magenta",justify="center")
    # table.add_column("Director", justify="center", style="green")

    table.add_row("1", "食物信息查询")
    table.add_row("2", "冰箱状态查询")
    table.add_row("3", "食品管理")
    table.add_row("4", "使用摄像头录入食品")
    table.add_row("5", "扫描生鲜类食品二维码")
    console.print(table)
    a = input()
    # a = await ainput()#异步输入
    a = int(a)
    select_modle(a)
    
def select_modle(a):
    
    if not(a > 0 and a <=5):
        print('输入错误，请重新输入')
        b = input()
        b = int(b)
        select_modle(b)
    if a == 1:
            console.clear()
            info = database.quary_food()
            console.print(f"[bold red]共查询到{len(info)}条食品信息[/bold red]")
            
            table = Table(title="食品信息查询界面")
            table.add_column("index", justify="center", style="cyan", no_wrap=True)
            table.add_column("食品名称", justify="center", style="magenta")
            table.add_column("食品类别", justify="center", style="green")
            table.add_column("创建时间", justify="center", style="red")
            table.add_column("修改时间", justify="center", style="yellow")
            
            for row in info:
                table.add_row(str(row[0]), row[1], str(row[2]),str(row[-2]),str(row[-1]))
            
            console.print(table)
            
    elif a == 2:
            console.clear()
            info = database.quary_device()
            console.print(f"[bold red]当前设备信息[/bold red]")
            
            table = Table(title="设备当前信息")
            table.add_column("index", justify="center", style="cyan", no_wrap=True)
            table.add_column("时间", justify="center", style="magenta")
            table.add_column("温度", justify="center", style="green")
            table.add_column("湿度", justify="center", style="red")
            table.add_column("二氧化碳", justify="center", style="yellow")
            
            # for row in info:
            table.add_row(str(info[-1][0]), str(info[-1][1]), str(info[-1][2]), str(info[-1][3]), str(info[-1][4]))
            console.print(table)
            
    elif a == 3:
            console.clear()
            console.print(f"[bold red]请问要食品入库(按1)还是食品出库(按2)[/bold red]")
            
            while True:
                next = input()
                next = int(next)
                
                if next == 1:
                    console.clear()
                    info = []
                    name = input('请输入要录入的食品名称')
                    print('请输入录入的食品类别')
                    type = input()
                    current_time = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime())
                    info.append(name)
                    info.append(type)
                    info.append(current_time)
                    QR(info)
                    # ASYNC_CACHE.append(['add_food',name,type])
                    database.add_food(name, type, "./images/QR/{}.jpg".format(current_time))
                    
                    break
                elif next == 2:
                    console.clear()
                    #######显示库存食品########
                    info = database.quary_food()
                    console.print(f"[bold red]共查询到{len(info)}条食品信息[/bold red]")
                    
                    table = Table(title="食品信息查询界面")
                    table.add_column("index", justify="center", style="cyan", no_wrap=True)
                    table.add_column("食品名称", justify="center", style="magenta")
                    table.add_column("食品类别", justify="center", style="green")
                    table.add_column("创建时间", justify="center", style="red")
                    table.add_column("修改时间", justify="center", style="yellow")
                    for row in info:
                        table.add_row(str(row[0]), row[1], str(row[2]),str(row[-2]),str(row[-1]))
                    console.print(table)
                    
                    id = input('请输入要出库的食品的index')
                    # ASYNC_CACHE.append(['del_food', id])
                    database.del_food(index = id)

                    break
 
                else:
                    print('请重新输入')
            
            
    elif a == 4:
        cap = cv2.VideoCapture(0)  

            # 检查摄像头是否成功打开
        if not cap.isOpened():
            print("无法打开摄像头")
            exit()
        try:
            while True:
        # 捕获 frame-by-frame
                ret, frame = cap.read()
                if not ret:
                    print("无法接收帧，退出...")
                    break
                cv2.imshow('Frame', frame)
                
                
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    name = './images/{}.jpg'.format(time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime()))
                    cv2.imwrite(name,frame)
                    print('photo saved')
                    client(name)
                    
                # 按 'q' 退出
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
    # 当一切完成后，释放捕获
            cap.release()
            cv2.destroyAllWindows()
            
    elif a == 5:
        scan()
        
    console.print(f"[bold red]按任意键回到上一界面[/bold red]")
    next = input()
    hello_console()

#更新设备信息循环任务
def cycle_work():
    humidity, temperature = cond()
    database.update_device(humidity,temperature)
    print('设备信息一更新')
    
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cycle_work, 'interval', seconds=60)
    scheduler.start()
    try:
        while True:
            pass
    except(KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    console = Console()
    #数据库实例化
    database = Database()
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.start()
    #开始界面
    hello_console()

    database.connection.close()


