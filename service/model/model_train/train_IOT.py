import torch
from PIL import Image
from torchvision import transforms
from torchvision import datasets
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
import torchvision
from torch import nn
from datasets import Datasets


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

#获取数据集
# train_data = datasets.CIFAR10(root='./data',train=True,transform=transforms.ToTensor(),
#                               download=True)
# test_data = datasets.CIFAR10(root='./data',train=False,transform=transforms.ToTensor(),
#                              download=True)
transform = transforms.Compose([transforms.Resize((256,256)),transforms.ToTensor()])
train_data = Datasets(train_set=True,transform=transform)
test_data = Datasets(transform=transform)

#创建网络模型
class Tudui(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3,32,kernel_size=3,stride=1,padding=1),
            nn.MaxPool2d(2),
            nn.Conv2d(32,32,5,1,2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,32,5,1,2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,64,5,1,2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64*16*16,64),
            nn.Linear(64,11)
        )
        
    def forward(self,x):
        x = self.model(x)
        return x

#获取数据集长度
train_data_size = len(train_data)
test_data_size = len(test_data)
print('训练数据集的长度:{}'.format(train_data_size))
print('测试数据集的长度:{}'.format(test_data_size))

#利用dataloader加载数据集
train_dataloader = DataLoader(train_data,batch_size=128)
test_dataloader = DataLoader(test_data,batch_size=128)

#创建网络模型
tudui = Tudui()
tudui = tudui.to(device)

#损失函数
loss_fn = nn.CrossEntropyLoss()
loss_fn = loss_fn.to(device)

#优化器
learning_rating = 0.01
optimizer = torch.optim.Adam(tudui.parameters(),lr=learning_rating)

#设置训练网络的参数
total_train_step = 0    #记录训练的次数
total_test_step = 0    #记录测试的次数
epoch = 80  #训练的轮数

#添加tensorboard
writer = SummaryWriter('./logs_train',)

for i in range(epoch):
    print('_'*10,'第 {} 轮开始训练'.format(i+1),'_'*10)
    
    tudui.train()   #如果网络中有dropout、batchnorm一定要写，否则可有可无
    for data in train_dataloader:
        img, target = data
        img = img.to(device)
        target = target.to(device)
        output = tudui(img)
        loss = loss_fn(output, target)

        #优化器优化模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_train_step = total_train_step + 1
        if total_train_step % 100 == 0:
            print('训练第 {} 轮，训练次数：{}，Loss：{}'.format(i+1, total_train_step,loss.item()))
            writer.add_scalar('train_loss', loss.item(), total_train_step)

    #测试步骤
    tudui.eval() #如果网络中有dropout、batchnorm一定要写，否则可有可无
    total_test_loss = 0
    total_accuracy = 0
    with torch.no_grad():
        for data in test_dataloader:
            img, target = data
            img = img.to(device)
            target = target.to(device)
            output = tudui(img)
            loss = loss_fn(output,target)
            total_test_loss = total_test_loss + loss.item()
            accuracy = (output.argmax(1) == target).sum()
            total_accuracy = total_accuracy + accuracy
    
    print('整体测试集上的loss：{}'.format(total_test_loss/test_data_size*64))
    print('整体测试集上的准确率：{}'.format(total_accuracy / test_data_size))
    writer.add_scalar('test_acc', total_accuracy / test_data_size, total_test_step)
    writer.add_scalar('test_loss',total_test_loss,total_test_step)
    total_test_step = total_test_step + 1

    torch.save(tudui,"tudui_{}.pth".format(i))
    print('模型以保存')

writer.close()

