#!/bin/bash

echo "Creating model archive. If synthdet.mar exists in the current directory, it will be overwritten"
torch-model-archiver --model-name synthdet --version 1.0 --model-file synthdet.py --serialized-file synthdet_faster_rcnn.pth --handler synthdet_model_handler.py --extra-files index_to_name.json --force
