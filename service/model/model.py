import torch
from torch import nn
from torchvision import transforms
from PIL import Image

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

def predict(path:str):
    device = torch.device("cpu")
    model = torch.load('/root/IOT/py/vgg16/tudui_68---96.4%.pth', map_location=torch.device('cpu'))
    state_dict = model.state_dict()
    
    new_model = Tudui()
    new_model.load_state_dict(state_dict)
    new_model.to(device)

    
    model.eval()
    # input_path = '2_1036.jpg'
    input_path = path
    img = Image.open(input_path)
    transform = transforms.Compose([transforms.Resize((256,256)),transforms.ToTensor()])

    img = transform(img).unsqueeze(0)
    img.to(device)
    
    # print(img.shape)
    
    output = new_model(img)
    target = torch.argmax(output)
    print(target)
    return target

if __name__ == '__main__':
    predict('2_1036.jpg')
  
