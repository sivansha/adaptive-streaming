#!/bin/bash

# pase a network trace or a network speed at command line




if [ $# -eq 0 ]
  then
    echo ""
    echo "The bashscript shapes the current network either by providing a"
    echo "static value in MB/s or by providing the path to a network trace."
    echo ""
    echo "   [*] -d [path/to/dynamic_trace]"
    echo "   [*] -s [static_value]"
    echo ""

    exit 0
fi

if [ "$1" == "-s" ] && [ ! -z "$2" ]; then
    echo "   [*] Using static profile..."
    sudo ip netns exec ns_srv0 tc class change dev ns_srv0_veth0 parent 1: classid 1:1 htb rate ${2}Mbit
    exit 0
fi

if [ "$1" == "-d" ] && [ ! -z "$2" ]; then
    echo "   [*] Using dynamic profile..."
    filename="$2"
    while read -r line; do
        value="$line"
        sudo ip netns exec ns_srv0 tc class change dev ns_srv0_veth0 parent 1: classid 1:1 htb rate ${value}kbit
        sleep 1
    done < "$filename"
    exit 0
fi

exit 1