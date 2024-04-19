#!/bin/bash

for service in raspberry-access-door1.service \
               raspberry-access-door2.service \
               raspberry-access-door3.service \
               raspberry-access-door4.service
do
    if systemctl --no-pager is-enabled $service
    then
        systemctl restart $service
    fi
done
