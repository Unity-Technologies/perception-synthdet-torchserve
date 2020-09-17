## GPU Performance
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

## Internet Latency
As with any network request, there is time overhead in sending data to and from the server. Your results may significantly vary from ours in this area, depending on proximity to the server, WiFi speeds, ISP speeds, and many more factors. Try to aim for a total request time of ~1000 ms or less (that includes model inference time).
