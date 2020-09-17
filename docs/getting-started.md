## Getting Started
It is highly encouraged that you run TorchServe on a computer with CUDA capability, since prediction times will be unusable when predicting on a CPU (around 3 seconds of inference time). Make sure the latest CUDA drivers are installed. Cloud services such as [AWS](https://aws.amazon.com/marketplace/pp/Amazon-Web-Services-Deep-Learning-AMI-Ubuntu-1604/B077GCH38C) and [Google Cloud](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning) provide VM images pre-configured to support CUDA. If running in the cloud, it is easiest to start with one of those. For RAM, 16 GB will work fine. Check out our deploy guides for [AWS](https://github.com/Unity-Technologies/perception-synthdet-torchserve/wiki/Deploying-a-CUDA-enabled-AWS-VM-Instance) and [Google Cloud Platform](https://github.com/Unity-Technologies/perception-synthdet-torchserve/wiki/Deploying-a-CUDA-enabled-GCP-VM-Instance) VM instances.

### Configuring your machine
1. Copy your SynthDet serialized PyTorch model file into your cloned repository, and name it `synthdet_faster_rcnn.pth`. If you are using a custom model, read the [Adapting for your Model](https://github.com/Unity-Technologies/perception-synthdet-torchserve/wiki/Adapting-for-your-Model) wiki page.
2. Copy this entire directory onto the machine that will host TorchServe.
3. Make scripts executable: `chmod +x archive.sh build.sh configure.sh launch.sh qr.sh`
4. If your machine has `apt-get`, you can run `./configure.sh` which will prepare everything to launch TorchServe.

### Starting TorchServe
If you ran `configure.sh`, or completed the steps that it does, run `./launch.sh` from this directory and TorchServe will start. We recommend starting TorchServe in `tmux` since it fills its terminal with text output in the background.

### Stopping TorchServe
Run `torchserve --stop` to stop TorchServe. This can be run from any terminal on the machine.

### Accessing TorchServe
Submit a POST request to `/predictions/synthdet` with JPEG data of the requested image in the request body. If using `curl`, use the `-T` flag with the image as its value.
