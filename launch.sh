#!/bin/bash

torchserve --start --ncs --model-store model_store --models synthdet.mar
