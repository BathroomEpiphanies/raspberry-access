#!/bin/bash

/usr/bin/tmux "kill-session" -t "friskola-access-monitor"
/usr/bin/tmux "new-session" -d -s "friskola-access-monitor" -n "dashboard" -- "tail -f /var/log/friskola-access-door1.log"
/usr/bin/tmux "split-window" -t "friskola-access:dashboard" -v             -- "tail -f /var/log/friskola-access-door2.log"
/usr/bin/tmux "split-window" -t "friskola-access:dashboard" -v             -- "tail -f /var/log/friskola-access-door3.log"
/usr/bin/tmux "split-window" -t "friskola-access:dashboard" -v             -- "tail -f /var/log/friskola-access-door4.log"
/usr/bin/tmux "select-layout" "even-vertical"
tmux attach
