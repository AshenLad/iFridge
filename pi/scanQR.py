import cv2
from pyzbar import pyzbar

def scan():
    
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 0 通常是默认的摄像头编号，如果有多个设备，可能需要更改

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()

    try:
        while True:
            # 捕获 frame-by-frame
            ret, frame = cap.read()

            # 如果正确读取帧，ret 为 True
            if not ret:
                print("无法接收帧，退出...")
                break

            # 显示结果帧
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Frame', frame)
            
            barcodes = pyzbar.decode(frame)
            if barcodes:
                print(barcodes[0][1])
                print(barcodes[0][0])
                break
            

            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # 当一切完成后，释放捕获
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    scan()