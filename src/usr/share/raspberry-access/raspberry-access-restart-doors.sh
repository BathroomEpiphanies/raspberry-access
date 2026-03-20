#!/bin/bash
trap IFS=$OLDIFS EXIT

OLDIFS=$IFS
IFS=$'\n'
services="$(systemctl list-units --no-pager --no-legend --plain --state 'loaded' --output 'json' 'raspberry-access@*.service' | jq -rc .[])"
for service in ${services[@]}
do
    unit="$(echo "${service}" | jq -rc .unit)"
    systemctl restart "${unit}"
done
