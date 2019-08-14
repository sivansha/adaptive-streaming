sudo apt-get install -y software-properties-common


sudo add-apt-repository -y ppa:mc3man/trusty-media
sudo apt-get update



sudo apt-get install -y python-twisted python-twisted-bin python-twisted-core python-twisted-web \
    gstreamer0.10-plugins-* gstreamer0.10-ffmpeg gstreamer0.10-tools python-gst0.1 libgstreamer0.10-dev \
    python-scipy python-psutil

sudo apt-get install -y gstreamer1.0-plugins*


sudo apt-get install -y apache2 

sudo cp -r /home/vagrant/test-content  /var/www/html
sudo cp -r /home/vagrant/content  /var/www/html

sudo ip netns add ns_clt0
sudo ip netns add ns_srv0

sudo ip link add ns_clt0_veth0 type veth peer name ns_srv0_veth0

sudo ip link set ns_clt0_veth0 netns ns_clt0
sudo ip link set ns_srv0_veth0 netns ns_srv0

sudo ip netns exec ns_clt0 ifconfig ns_clt0_veth0 192.168.10.1/24 up
sudo ip netns exec ns_srv0 ifconfig ns_srv0_veth0 192.168.10.2/24 up

sudo ip netns exec ns_srv0 sudo service apache2 restart

sudo ip netns exec ns_srv0 tc qdisc add dev ns_srv0_veth0 root handle 1: htb default 1
sudo ip netns exec ns_srv0 tc class add dev ns_srv0_veth0 parent 1: classid 1:1 htb rate 432.78Kbit 



sudo apt-get install python-twisted python-twisted-bin python-twisted-core python-twisted-web \
    gstreamer0.10-plugins-* gstreamer0.10-ffmpeg gstreamer0.10-tools python-gst0.1 libgstreamer0.10-dev \
    python-scipy python-psutil




#sudo ip netns exec ns_clt0 python tapas/play.py -m fake -u http://192.168.10.2/test-content/tos.m3u8