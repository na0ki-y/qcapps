'''
https://pystyle.info/pytorch-how-to-use-pretrained-model/
'''
import json
from pathlib import Path

import numpy as np
import torch
import torchvision
from PIL import Image
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.datasets.utils import download_url

def get_device(use_gpu):
    if use_gpu and torch.cuda.is_available():
        # これを有効にしないと、計算した勾配が毎回異なり、再現性が担保できない。
        torch.backends.cudnn.deterministic = True
        return torch.device("cuda")
    else:
        return torch.device("cpu")
    
def get_classes():
    if not Path("data_pytorch/imagenet_class_index.json").exists():
        # ファイルが存在しない場合はダウンロードする。
        download_url("https://git.io/JebAs", "data_pytorch", "imagenet_class_index.json")

    # クラス一覧を読み込む。
    with open("data_pytorch/imagenet_class_index.json") as f:
        data = json.load(f)
        class_names = [x["ja"] for x in data]

    return class_names


def prepara():
    # デバイスを選択する。
    device = get_device(use_gpu=True)
    model = torchvision.models.resnet50(pretrained=True).to(device)
    transform = transforms.Compose(
    [
        transforms.Resize(256),  # (256, 256) で切り抜く。
        transforms.CenterCrop(224),  # 画像の中心に合わせて、(224, 224) で切り抜く
        transforms.ToTensor(),  # テンソルにする。
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        ),  # 標準化する。
    ]
    )
    return device,model,transform

def mycovert(img,device,transform):
    img=img.convert('RGB')
    #img.show()
    inputs = transform(img)
    inputs = inputs.unsqueeze(0).to(device)
    return inputs
def myeval(inputs,model,):
    model.eval()
    outputs = model(inputs)
    # クラス名一覧を取得する。
    class_names = get_classes()
    batch_probs = F.softmax(outputs, dim=1)
    batch_probs, batch_indices = batch_probs.sort(dim=1, descending=True)
    eval_out=[]
    for probs, indices in zip(batch_probs, batch_indices):
        for k in range(3):
            eval_out.append(f"Top-{k + 1} {class_names[indices[k]]} {probs[k]:.2%}")
    return eval_out


def main():
    device,model,transform=prepara()

    img = Image.open("./image/irasutoya_character_apple.png").convert('RGB')
    inputs=mycovert(img,device,transform)
    eval_out=myeval(inputs,model,)
    for o in eval_out:
        print(o)
    
if __name__ == '__main__':
    main()