#!/bin/bash

for service in friskola-access-door1.service \
               friskola-access-door2.service \
               friskola-access-door3.service \
               friskola-access-door4.service
do
    if systemctl --no-pager is-enabled $service
    then
        systemctl restart $service
    fi
done
