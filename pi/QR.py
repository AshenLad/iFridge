import qrcode
from PIL import Image


def QR(data):
    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    # 创建一个二维码图像
    img = qr.make_image(fill='black', back_color='white')

    # 显示二维码
    # img.show()
    qr_data = str(data[0]) + ' ' + str(data[1]) + ' ' + str(data[2])
    # 如果需要保存二维码到文件
    img.save("./images/QR/{}.jpg".format(data[2]))
    # img.save('./qr.jpg')

if __name__ == '__main__':
    data = 'dhjksalkdjlasd'
    QR(data)