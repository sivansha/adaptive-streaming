alias la='ls -lisah'
alias myip='wget http://ipecho.net/plain -O - -q'
alias c='clear'
alias stream_test='sudo ip netns exec ns_clt0 python /home/vagrant/tapas/play.py -m fake -u http://192.168.10.2/test-content/tos.m3u8'
alias stream='sudo ip netns exec ns_clt0 python /home/vagrant/tapas/play.py -m fake -u http://192.168.10.2/content/big_buck_master.m3u8'

