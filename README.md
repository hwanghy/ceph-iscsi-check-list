# ceph-iscsi-check-list

# set hostname node1
  - sudo hostnamectl set-hostname ceph1

# set hostname node2
  - sudo hostnamectl set-hostname ceph2

# set hostname node3
  - sudo hostnamectl set-hostname ceph3

# edit file hosts all nodes
  - vi /etc/hosts
  > 10.0.0.1 ceph1
    10.0.0.2 ceph2
    10.0.0.3 ceph3

# Stop firewall all nodes
  - systemctl stop ufw
  - systemctl disable ufw

# Install chrony sync time
  - apt install chrony -y
  - systemctl start chronyd
  - systemctl enable chronyd
  
# make cephadm folder
  - mkdir cephadm
  - mkdir /etc/ceph
  - cd cephadm

# Install docker all nodes
  - https://docs.docker.com/engine/install/ubuntu/
  
# Use curl to fetch the most recent version of the standalone script:
  - curl --silent --remote-name --location https://github.com/ceph/ceph/raw/octopus/src/cephadm/cephadm
  - chmod +x cephadm
  
# add repo release cephadm all nodes
  - ./cephadm add-repo --release octopus
  - wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
  - apt-get update
  - rm /etc/apt/trusted.gpg.d/ceph.release.gpg
  - ./cephadm install
  
# comfirm cephadm is now in your path
  - which cephadm
    
# install ceph services all nodes.
  - apt-get update 
  - cephadm install ceph-mon ceph-osd ceph-mgr ceph-common
  
# bootstrap the cluster run the following command just the IP for the first cluster node.
  # run this command if have more 1 NIC and config Mon ip later after bootstrap finished.
  - cephadm bootstrap --mon-ip 192.168.1.41
  - ceph config set mon public_network 192.168.1.0/24
  - ceph config set mon cluster_network 10.0.0.0/8
  # Save bootstrap info
  > URL: https://ceph1:8443/
	    User: admin
	  Password: b3h3p8vz49
# INFO:cephadm:You can access the Ceph CLI with:
  > cephadm shell
# Add hosts to the cluster
  - ssh-copy-id -f -i /etc/ceph/ceph.pub root@new-host
  
# Copy config & Keyring to other nodes
  - scp /etc/ceph/* root@new-host:/home
  
# install config
  - cd /home
  - sudo install -m 0644 ceph.conf /etc/ceph/ceph.conf
  - sudo install -m 0600 ceph.client.admin.keyring /etc/ceph/ceph.keyring
  
# add ceph node is part cluster
  - ceph orch host add new-host
  
# verify nodes in cluster
  - ceph orch host ls
  
# adjust the default of 3 monitor
  - ceph orch apply mon 3
  
# adjust the default of 3 mgr
  - ceph orch apply mgr 3
  
#  To set the mon label( Must have the first node)
  - ceph orch host label add *<hostname>* mon
  
# To view the current hosts and labels:
  - ceph orch host ls
  
# Tell cephadm to deploy monitors based on the label:
  - ceph orch apply mon label:mon

# Config osd pool default size for 2 nodes
  - ceph config set global osd_pool_default_size 2
  - ceph config set global osd_pool_default_min_size 1
  
# add config cluster mon
  - vi /etc/ceph/ceph.conf
  > mon_host = [v2:192.168.1.41:3300/0,v1:192.168.1.41:6789/0] [v2:192.168.1.42:3300/0,v1:192.168.1.42:6789/0] [v2:192.168.1.43:3300/0,v1:192.168.1.43:6789/0]

# deploy iscsi target 

# Config osd node storage cluster for iscsi
  - ceph tell osd.0 config set osd_heartbeat_grace 20
  - ceph tell osd.0 config set osd_heartbeat_interval 5
  
# Install ceph-iscsi
  - apt install ceph-iscsi
  - systemctl daemon-reload
  - systemctl enable rbd-target-gw
  - systemctl start rbd-target-gw
  - systemctl enable rbd-target-api
  - systemctl start rbd-target-api
  
# fix crash python3
  - https://github.com/ceph/ceph-iscsi/commit/e48dcb0d3099b27595b9f4433da8493f5edb9206#diff-f1381af4114a1e777ef5e8b7b7452a01
  
# Create iqn target
  - gwcli
  - cd /iscsi-targets
  - create iqn.2020-08.vndata.vn.iscsi-gw:iscsi-igw
  - cd iqn.2020-08.vndata.vn.iscsi-gw:iscsi-igw/gateways
  - create ceph1 192.168.1.41
  - create ceph2 192.168.1.42
  - cd /disks
  > create image with pool rbd
  - create pool=rbd image=disk_1 size=90G
  > Create client with initiator name
  - cd hosts/
  - create iqn.2020-08.vndata.vn.client:vndata-client
  > Create Chap username and password
  - auth username=huy password =huy
  > Add disk to client
  - disk add rbd/disk_1
  
# Install iscsi-gateway dashboard
  - ceph dashboard set-iscsi-api-ssl-verification false
  - ceph dashboard iscsi-gateway-add http://admin:admin@192.168.1.41:5000
  - ceph dashboard iscsi-gateway-add http://admin:admin@192.168.1.42:5000
  - ceph dashboard iscsi-gateway-list
  > remove gateway
  - ceph dashboard iscsi-gateway-rm GATEWAY_NAME
