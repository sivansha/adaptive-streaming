#!/bin/bash

# script to run all the streams for q3
mkdir live_logs tapas_logs
for network in 0.5 1 2
do

    echo " [!!!] starting with stream with ${network}Mbit/s"

    for i in 1 2 3 4 5
    do
        echo "   [*]"
        echo "   [*] Round $i starting with stream with ${network}Mbit/s"
        echo ""
        ~/run_trace.sh -s ${network}&
        sudo ip netns exec ns_clt0 python /home/vagrant/tapas/play.py -m fake -u http://192.168.10.2/ml_bbb_240s/bbb.m3u8|tee live_logs/live_log_static_${network}_round_${i}.log
        ls -lt /home/vagrant/tapas/logs/conventional|head -2|tail -1|xargs -I '{}' cp /home/vagrant/tapas/logs/conventional/'{}' tapas_logs/tapas_conventional_log_static_${network}_round_${i}.log
        #sleep 600
    done
done

for network in network_trace0 network_trace1 network_trace2
do

    echo " [!!!] starting with stream with dynamic ${network}"

    for i in 1 2 3 4 5
    do
        echo "   [*]"
        echo "   [*] Round $i starting with stream with dynamic ${network}"
        echo ""
        ~/run_trace.sh -d /home/vagrant/traces/${network}&
        sudo ip netns exec ns_clt0 python /home/vagrant/tapas/play.py -m fake -u http://192.168.10.2/ml_bbb_240s/bbb.m3u8|tee live_logs/live_log_dynomic_${network}_round_${i}.log
        ls -lt /home/vagrant/tapas/logs/conventional|head -2|tail -1|xargs -I '{}' cp /home/vagrant/tapas/logs/conventional/'{}' tapas_logs/tapas_conventional_log_dynamic_${network}_round_${i}.log
        #sleep 600
    done
done
