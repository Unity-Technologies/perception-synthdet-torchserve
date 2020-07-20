# Unity SynthDet on TorchServe

## About
As part of the Unity SynthDet Demo App project, we found it best to host a trained ML model running in PyTorch in the cloud, and expose a REST API to communicate with a mobile device used for capturing images. For hosting this REST API, we went with [TorchServe](https://github.com/pytorch/serve). TorchServe takes an ML model, runs it in PyTorch, and exposes an endpoint used for predictions.

## Getting Started
It is highly encouraged that you run TorchServe on a computer with CUDA capability, since prediction times will be unusable when predicting on a CPU (around 3 seconds of inference time). Make sure the latest CUDA drivers are installed. Cloud services such as [AWS](https://aws.amazon.com/marketplace/pp/Amazon-Web-Services-Deep-Learning-AMI-Ubuntu-1604/B077GCH38C) and [Google Cloud](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning) provide VM images pre-configured to support CUDA. If running in the cloud, it is easiest to start with one of those. For RAM, 16 GB will work fine. Check out our deploy guides for [AWS](https://github.com/Unity-Technologies/perception-synthdet-torchserve/wiki/Deploying-a-CUDA-enabled-AWS-VM-Instance) and [Google Cloud Platform](https://github.com/Unity-Technologies/perception-synthdet-torchserve/wiki/Deploying-a-CUDA-enabled-GCP-VM-Instance) VM instances.

### GPU Performance
We recommend you run SynthDet on a CUDA-enabled GPU that has inference times of 150 ms or less. If using Google Cloud, the Nvidia Tesla T4 will work fine. These are the GPUs that have been tested so far:
| GPU | Average Inference Time\* | Cloud Platform | Hourly VM Cost |
| --- | ----------------------- | -------------- | -------------- |
| Nvidia Tesla M60 | 310 ms | AWS | $0.71 |
| Nvidia Tesla T4 | 125 ms | Google Cloud | $0.48 |
| Nvidia GeForce RTX 2080 Max-Q Design | 110 ms | Native\*\* | N/A |

\* Inference tests done with PyTorch on images with sizes near 1280x720 and 640x480. Size difference between 720p and standard definition had negligable impact on inference time.
<br/>
\*\* Test done on an Alienware M15 laptop.

Feel free to submit a PR with more test times :]

### Internet Latency
As with any network request, there is time overhead in sending data to and from the server. Your results may significantly vary from ours in this area, depending on proximity to the server, WiFi speeds, ISP speeds, and many more factors. Try to aim for a total request time of ~1000 ms or less (that includes model inference time).

### Configuring your machine
1. Copy your SynthDet serialized PyTorch model file into your cloned repository, and name it `synthdet_faster_rcnn.pth`.
2. Copy this entire directory onto the machine that will host TorchServe.
3. Make scripts executable: `chmod +x archive.sh build.sh configure.sh launch.sh`
4. If your machine has `apt-get`, you can run `./configure.sh` which will prepare everything to launch TorchServe.

### Scripts

| Script | Description |
| ------ | ----------- |
| `archive.sh` | Creates a TorchServe model archive and place it in the current directory |
| `build.sh` | Runs `archive.sh` and places the resulting model archive in the `model_store` folder, where TorchServe reads models from |
| `configure.sh` | Installs necessary dependencies, including TorchServe, then builds a TorchServe model archive |
| `cuda_check.py` | Checks if PyTorch has CUDA access |
| `launch.sh` | Starts TorchServe; run in `tmux` to prevent your terminal from getting flooded with text output |
| `qr.sh` | Prints QR codes for all model endpoints into your terminal; great for use with the Viewer app |
| `synthdet_model_test.py` | Tests the SynthDet model on an image specified as a parameter |

### Starting TorchServe
If you ran `configure.sh`, or completed the steps that it does, run `./launch.sh` from this directory and TorchServe will start. We recommend starting TorchServe in `tmux` since it fills its terminal with text output in the background.

### Stopping TorchServe
Run `torchserve --stop` to stop TorchServe. This can be run from any terminal on the machine.

### Accessing TorchServe
Submit a POST request to `/predictions/synthdet` with JPEG data of the requested image in the request body. If using `curl`, use the `-T` flag with the image as its value.

## Advanced Options
### Enabling HTTPS
By default, TorchServe accepts unencrypted HTTP requests, which is not optimal for privacy reasons, when sending real-life images over unencrypted HTTP. Because of this, we recommend configuring TorchServe to use HTTPS. You can provide your own SSL certificate, or create a self-signed one using [TorchServe's guide](https://pytorch.org/serve/configuration.html#id3).
