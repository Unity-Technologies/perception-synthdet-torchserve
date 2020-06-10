# Unity SynthDet on TorchServe

## About
As part of the Unity SynthDet Demo App project, we found it best to host a trained ML model running in PyTorch in the cloud, and expose a REST API to communicate with a mobile device used for capturing images. For hosting this REST API, we went with [TorchServe](https://github.com/pytorch/serve). TorchServe takes an ML model, runs it in PyTorch, and exposes an endpoint used for predictions.

## Getting Started
It is highly encouraged that you run TorchServe on a computer with CUDA capability, since prediction times will be unusable when predicting on a CPU (around 3 seconds of inference time). Make sure the latest CUDA drivers are installed. Cloud services such as [AWS](https://aws.amazon.com/marketplace/pp/Amazon-Web-Services-Deep-Learning-AMI-Ubuntu-1604/B077GCH38C) and [Google Cloud](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning) provide VM images pre-configured to support CUDA. If running in the cloud, it is easiest to start with one of those. For RAM, 16 GB will work fine.

### GPU Performance
We recommend you run SynthDet on a CUDA-enabled GPU that has inference times of 150 ms or less. If using Google Cloud, the Nvidia Tesla T4 will work fine. These are the GPUs that have been tested so far:
| GPU | Average Inference Time\* | Cloud Platform | Hourly VM Cost |
| --- | ----------------------- | -------------- | -------------- |
| Nvidia Tesla M60 | 310 ms | AWS | $0.71 |
| Nvidia Tesla T4 | 125 ms | Google Cloud | $0.48 |
| Nvidia GeForce RTX 2080 Max-Q Design | 110 ms | Native\*\* | N/A |

\* Inference tests done with PyTorch on images with sizes near 1280x720 and 640x480. Size difference between 720p and standard definition had negligable impact on inference time.
\*\* Test done on an Alienware M15 laptop.

Feel free to submit a PR with more test times :]

### Internet Latency
As with any network request, there is time overhead in sending data to and from the server. Your results may significantly vary from ours in this area, depending on proximity to the server, WiFi speeds, ISP speeds, and many more factors. Try to aim for a total request time of ~1000 ms or less (that includes model inference time).

### Configuring your machine
1. Copy this entire directory onto the machine that will host TorchServe.
2. Copy your SynthDet serialized PyTorch model file into the same place, and name it `synthdet_faster_rcnn.pth`.
3. If your machine has `apt-get`, you can run `./configure.sh` (you may have to `chmod +x configure.sh` first). `configure.sh` will install necessary dependencies, including TorchServe, and it will build a TorchServe model archive.

### Other scripts
* `archive.sh` will create a TorchServe model archive and place it in the current directory
* `build.sh` will run `archive.sh` and place the resulting model archive in the `model_store` folder, where TorchServe reads models from
* `cuda_check.py` will check if PyTorch has CUDA access
* `synthdet_model_test.py` will test the SynthDet model on an image specified.


### Starting TorchServe
If the previous steps are completed, run `./launch.sh` from this directory and TorchServe will start. We recommend starting TorchServe in `tmux` since it fills its terminal with text output in the background.

### Accessing TorchServe
Submit a POST request to `/predictions/synthdet` with JPEG data of the requested image in the request body. If using `curl`, use the `-T` flag with the image as its value.

## Advanced Options
### Enabling HTTPS
By default, TorchServe accepts unencrypted HTTP requests, which is not optimal for privacy reasons, when sending real-life images over unencrypted HTTP. Because of this, we recommend configuring TorchServe to use HTTPS. You can provide your own SSL certificate, or create a self-signed one using [TorchServe's guide](https://pytorch.org/serve/configuration.html#id3).
