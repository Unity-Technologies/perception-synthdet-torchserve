| Script | Description |
| ------ | ----------- |
| `archive.sh` | Creates a TorchServe model archive and place it in the current directory |
| `build.sh` | Runs `archive.sh` and places the resulting model archive in the `model_store` folder, where TorchServe reads models from |
| `configure.sh` | Installs necessary dependencies, including TorchServe, then builds a TorchServe model archive |
| `cuda_check.py` | Checks if PyTorch has CUDA access |
| `launch.sh` | Starts TorchServe; run in `tmux` to prevent your terminal from getting flooded with text output |
| `qr.sh` | Prints QR codes for all model endpoints into your terminal; great for use with the Viewer app |
| `synthdet_model_test.py` | Tests the SynthDet model on an image specified as a parameter |

Note: `qr.sh` assumes you are hosting through your public IP address. If you want to stick with your internal IP address (if self-hosting), or manually want to generate QR codes, you can use the python tool `segno <url>` installed earlier.