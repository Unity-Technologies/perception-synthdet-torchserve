#!/bin/bash

if [ ! -e model_store ]; then
    mkdir model_store
fi

./archive.sh
mv synthdet.mar model_store/
