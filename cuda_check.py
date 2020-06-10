import torch

if torch.cuda.is_available():
    print("CUDA is available")
else:
    print("CUDA is not available to PyTorch. For best results, install the latest CUDA toolkit")
    