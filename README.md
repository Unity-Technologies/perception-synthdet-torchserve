# Unity SynthDet on TorchServe
---

## About
As part of the Unity SynthDet Demo App project, we found it best to host a trained ML model running in PyTorch in the cloud, and expose a REST API to communicate with a mobile device used for capturing images. For hosting this REST API, we went with [TorchServe](https://github.com/pytorch/serve). TorchServe takes an ML model, runs it in PyTorch, and exposes an endpoint used for predictions.

## Getting Started
It is highly encouraged that you run TorchServe on a computer with CUDA capability, since prediction times will be unusable when predicting on a CPU (around 3 seconds of inference time). Make sure the latest CUDA drivers are installed. Cloud services such as [AWS](https://aws.amazon.com/marketplace/pp/Amazon-Web-Services-Deep-Learning-AMI-Ubuntu-1604/B077GCH38C) and [Google Cloud](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning) provide VM images pre-configured to support CUDA. If running in the cloud, it is easiest to start with one of those. For RAM, 16 GB will work fine.

### GPU Performance
We reccomend you run SynthDet on a CUDA-enabled GPU that has inference times of 150 ms or less. If using Google Cloud, the Nvidia Tesla T4 will work fine.

### Configuring your machine
1. Copy this entire directory onto the machine that will host TorchServe.
2. Copy your SynthDet serialized PyTorch model file into the same place, and name it `synthdet_faster_rcnn.pth`.
3. If your machine has `apt-get`, you can run `./configure.sh` (you may have to `chmod +x configure.sh` first). `configure.sh` will install necessary dependencies, including TorchServe, and it will build a TorchServe model archive.

### Other scripts
`archive.sh` will create a TorchServe model archive and place it in the current directory.
`build.sh` will run `archive.sh` and place the resulting model archive in the `model_store` folder, where TorchServe reads models from.

### Starting TorchServe
If the previous steps are completed, run `./launch.sh` from this directory and TorchServe will start. We reccomend starting TorchServe in `tmux` since it fills its terminal with text output in the background.

