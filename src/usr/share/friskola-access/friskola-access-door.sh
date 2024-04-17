#!/bin/bash

database="$1"
doornum="$2"

type="$(jq -rc ".[\"$(hostname)\"] | .\"type\"" /usr/local/etc/doors.json)"
door="$(jq -rc ".[\"$(hostname)\"] | .\"doors\" | .\"${doornum}\"" /usr/local/etc/doors.json)"


if [ "${door}" != "null" ]
then
    name="$(echo ${door} | jq -rc ".name")"
    reader="$(echo ${door} | jq -rc ".reader")"
    /usr/bin/${reader}_door \
        --system-type "${type}" \
        --door-number "${doornum}" \
        --door-name   "${name}" \
        --database    "${database}"
else
    echo "No door ${doornum}"
    read
fi
