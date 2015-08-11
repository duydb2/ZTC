#!/bin/bash

# WAN=${1:-wlan0}
# LAN=${2:-wlan1}

function title {
    echo
    echo "######### $1 #########"
    echo
}

function run_cmd {
    title "$1"
    $1
}

for cmd in "cat /etc/os-release" "pip freeze" "ip a" "ip r" "iptables-save"
do
    run_cmd "${cmd}"
done

for netif in ${IWAN} ${ILAN}
do
    for object in qdisc class filter
    do
        cmd="tc ${object} show dev ${netif}"
        run_cmd "${cmd}"
    done
done
