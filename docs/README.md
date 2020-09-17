# Unity SynthDet on TorchServe

## About
As part of the Unity SynthDet Viewer App project, we found it best to host a trained ML model running in PyTorch in the cloud, and expose a REST API to communicate with a mobile device used for capturing images. For hosting this REST API, we went with [TorchServe](https://github.com/pytorch/serve). TorchServe takes an ML model, runs it in PyTorch, and exposes an endpoint used for predictions.

* [Getting Started](https://github.com/Unity-Technologies/perception-synthdet-torchserve/blob/master/docs/getting-started.md)
* [Performance and Latency](https://github.com/Unity-Technologies/perception-synthdet-torchserve/blob/master/docs/performance-and-latency.md)
* [Scripts](https://github.com/Unity-Technologies/perception-synthdet-torchserve/blob/master/docs/scripts.md)
* [Advanced Options](https://github.com/Unity-Technologies/perception-synthdet-torchserve/blob/master/docs/enabling-https.md)

## License
* [License](https://github.com/Unity-Technologies/perception-synthdet-torchserve/blob/master/LICENSE.md)
