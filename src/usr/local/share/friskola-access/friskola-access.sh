#!/bin/bash

/usr/bin/tmux "kill-session" -t "friskola-access"

type="$(jq -rc ".[\"$(hostname)\"] | .\"type\"" /usr/local/etc/doors.json)"

door="$(jq -rc ".[\"$(hostname)\"] | .\"doors\" | .\"1\"" /usr/local/etc/doors.json)"
if [ "${door}" != "null" ]
then
    name="$(echo ${door} | jq -rc ".name")"
    reader="$(echo ${door} | jq -rc ".reader")"
    /usr/bin/tmux "new-session" -d -s "friskola-access" -n "dashboard"   -- "python3 /usr/local/share/friskola-access/${reader}_door.py --system-type ${type} --door-number 1 --door-name ${name} --database /usr/local/etc/access.sqlite | tee -a /var/log/${name}.log"
else
    /usr/bin/tmux "new-session" -d -s "friskola-access" -n "dashboard"   -- "watch -n 600 echo 'No door 1'"
fi

door="$(jq -rc ".[\"$(hostname)\"] | .\"doors\" | .\"2\"" /usr/local/etc/doors.json)"
/usr/bin/tmux "select-window" -t "friskola-access:dashboard"
/usr/bin/tmux "select-pane" -t "0"
if [ "${door}" != "null" ]
then
    name="$(echo ${door} | jq -rc ".name")"
    reader="$(echo ${door} | jq -rc ".reader")"
    /usr/bin/tmux "split-window" -t "friskola-access:dashboard" -v -p 50 -- "python3 /usr/local/share/friskola-access/${reader}_door.py --system-type ${type} --door-number 2 --door-name ${name} --database /usr/local/etc/access.sqlite | tee -a /var/log/${name}.log"
else
    /usr/bin/tmux "split-window" -t "friskola-access:dashboard" -v -p 50 -- "watch -n 600 echo 'No door 2'"
fi

door="$(jq -rc ".[\"$(hostname)\"] | .\"doors\" | .\"3\"" /usr/local/etc/doors.json)"
/usr/bin/tmux "select-window" -t "friskola-access:dashboard"
/usr/bin/tmux "select-pane" -t "0"
if [ "${door}" != "null" ]
then
    name="$(echo ${door} | jq -rc ".name")"
    reader="$(echo ${door} | jq -rc ".reader")"
    /usr/bin/tmux "split-window" -t "friskola-access:dashboard" -h -p 50 -- "python3 /usr/local/share/friskola-access/${reader}_door.py --system-type ${type} --door-number 3 --door-name ${name} --database /usr/local/etc/access.sqlite | tee -a /var/log/${name}.log"
else
    /usr/bin/tmux "split-window" -t "friskola-access:dashboard" -h -p 50 -- "watch -n 600 echo 'No door 3'"
fi

door="$(jq -rc ".[\"$(hostname)\"] | .\"doors\" | .\"4\"" /usr/local/etc/doors.json)"
/usr/bin/tmux "select-window" -t "friskola-access:dashboard"
/usr/bin/tmux "select-pane" -t "2"
if [ "${door}" != "null" ]
then
    name="$(echo ${door} | jq -rc ".name")"
    reader="$(echo ${door} | jq -rc ".reader")"
    /usr/bin/tmux "split-window" -t "friskola-access:dashboard" -h -p 50 -- "python3 /usr/local/share/friskola-access/${reader}_door.py --system-type ${type} --door-number 4 --door-name ${name} --database /usr/local/etc/access.sqlite | tee -a /var/log/${name}.log"
else
    /usr/bin/tmux "split-window" -t "friskola-access:dashboard" -h -p 50 -- "watch -n 600 echo 'No door 4'"
fi
