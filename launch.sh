#!/bin/bash

source config.properties

torchserve --start --ncs --model-store $model_store
