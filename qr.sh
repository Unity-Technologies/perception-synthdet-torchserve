#!/bin/bash

source config.properties

IP=$(curl -s icanhazip.com)
# Get port number from host with port: https://stackoverflow.com/questions/6174220/parse-url-in-shell-script
PORT=$(echo $inference_address | sed -e 's,^.*:,:,g' -e 's,.*:\([0-9]*\).*,\1,g' -e 's,[^0-9],,g')

SECURE=""
if [[ $inference_address =~ ^https+ ]]; then
    SECURE="s"
fi

function print_qr {
    url=http$SECURE://$IP:$PORT/predictions/$1
    echo "$1 - $url"
    segno $url
    printf "\n\n\n"
}

while read line
do
    print_qr $(basename $line .mar)
done < <(ls $model_store)
