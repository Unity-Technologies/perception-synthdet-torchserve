#!/bin/bash

IP=$(curl -s icanhazip.com)
source config.properties

SECURE=""
if [[ $inference_address =~ ^https+ ]]; then
    SECURE="s"
fi

function print_qr {
    url=http$SECURE://$IP/predictions/$1
    echo "$1 - $url"
    segno $url
    printf "\n\n\n"
}

while read line
do
    print_qr $(basename $line .mar)
done < <(ls $model_store)
