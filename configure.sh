#!/bin/bash

echo "Please read and answer 'yes' to prompts"

echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install openjdk-11-jdk
sudo apt-get install python3-pip

pip3 install torch torchtext torchvision sentencepiece psutil future yacs
pip3 install torchserve torch-model-archiver segno

echo "Checking for CUDA..."
python3 ./cuda_check.py

echo "Creating model_store..."
./build.sh

echo "All set! Run ./launch.sh to start TorchServe"
