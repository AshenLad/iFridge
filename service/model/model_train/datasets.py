from torchvision import datasets,transforms
from torch.utils.data import Dataset,DataLoader
from PIL import Image
import os
import numpy as np
from torch.utils.tensorboard import SummaryWriter
from torchvision.utils import make_grid
import torch


writer = SummaryWriter('logs')
class Datasets(Dataset):
    def __init__(self,train_set = True,transform = None):
        self.path = './data/food-11'
        self.transform = transform
        if train_set:
            self.path = os.path.join(self.path,'training')
        else:
            self.path = os.path.join(self.path, 'validation')
        self.set_list = os.listdir(self.path)

        self.train_label = []
        self.val_path = []

    def __getitem__(self,index):
        label, _ = self.set_list[index].split('_')
        image_path = os.path.join(self.path,self.set_list[index])
        img = Image.open(image_path)
        # img = np.array(img)

        if self.transform:
            img = self.transform(img)
        label = torch.tensor(int(label))
        return img, label
    
    def __len__(self):
        return len(self.set_list)

if __name__ == '__main__':
    transform = transforms.Compose([transforms.Resize((32,32)),transforms.ToTensor()])
    # # transform = transforms.Compose([transforms.ToTensor()])
    dataset = Datasets(transform = transform)
    dataloader = DataLoader(dataset,batch_size=64,shuffle=True)

    for i, j in enumerate(dataloader):
        img, label = j
        print(img, label)
        print(img.shape,label.shape)
        break
    #     # writer.add_image("image",make_grid(img),i)
    # writer.close()

    # dataset = Datasets(train_set=True)
    # print(len(dataset))
    # print(dataset[0])

