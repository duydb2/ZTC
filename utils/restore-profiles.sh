#!/usr/bin/env bash

ATC_HOST="$1"

if [ -z "$ATC_HOST" ] ; then
    echo "usage: $0 HOST"
    echo "    HOST should be of the form <hostname>:<port>"
    echo "    e.g. localhost:8080"
    exit 1
fi

for x in $(git rev-parse --show-toplevel)/utils/profiles/*.json ; do
    profile_id=$(cat ${x} | python -c 'import sys, json; print(json.load(sys.stdin)["id"])')
    out=$(curl -H "Content-Type: application/json" -X POST --silent http://"$ATC_HOST"/api/v1/profiles/${profile_id}/ -d "@${x}")
    rc="$?"
    if [ "$rc" -ne "0" ] ; then
        echo "Could not add profile $x (curl exit code $rc)"
        if [ -n "$out" ] ; then
            echo "$out"
            echo
        fi
    else
	echo "$out" > $x.html
        echo "Added profile $x"
    fi
done
