#!/bin/bash

for service in raspberry-access-door1.service \
               raspberry-access-door2.service \
               raspberry-access-door3.service \
               raspberry-access-door4.service \
               raspberry-access-door5.service \
               raspberry-access-door6.service \
               raspberry-access-door7.service \
               raspberry-access-door8.service
do
    if systemctl --no-pager is-active $service
    then
        systemctl stop $service
    fi
done
