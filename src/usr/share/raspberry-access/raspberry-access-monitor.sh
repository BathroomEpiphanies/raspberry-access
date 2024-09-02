#!/bin/bash

/usr/bin/tmux "kill-session" -t "raspberry-access-monitor"
/usr/bin/tmux "new-session" -d -s "raspberry-access-monitor" -n "dashboard"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door1.log"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door2.log"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door3.log"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door4.log"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door5.log"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door6.log"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door7.log"
/usr/bin/tmux "split-window" -t "raspberry-access:dashboard" -v             -- "tail -f /var/log/raspberry-access-door8.log"
/usr/bin/tmux "select-layout" "even-vertical"
tmux attach
