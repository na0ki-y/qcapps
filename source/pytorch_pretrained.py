import numpy as np
import torch
import torchvision

def get_device(use_gpu):
    if use_gpu and torch.cuda.is_available():
        # これを有効にしないと、計算した勾配が毎回異なり、再現性が担保できない。
        torch.backends.cudnn.deterministic = True
        return torch.device("cuda")
    else:
        return torch.device("cpu")

def main():
    # デバイスを選択する。
    device = get_device(use_gpu=True)
if __name__ == '__main__':
    main()