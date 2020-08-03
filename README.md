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

# Stop firewalld all nodes
  - systemctl stop firewalld
  - systemctl disable firewalld
# Disable selinux
  - vi /etc/selinux/config
  > SELINUX=disabled
  > reboot

# make cephadm folder
  - mkdir cephadm
  - mkdir /etc/ceph
  - cd cephadm

# Install docker all nodes
  - yum install epel-release -y
  - yum install docker -y
  - systemctl start docker
  - systemctl enable docker
  
# Use curl to fetch the most recent version of the standalone script:
  - curl --silent --remote-name --location https://github.com/ceph/ceph/raw/octopus/src/cephadm/cephadm
  - chmod +x cephadm
# install python3 all noes before install cephadm
  - yum install python3 -y
  
# add repo release cephadm all nodes
  - ./cephadm add-repo --release octopus
  - ./cephadm install
  
# comfirm cephadm is now in your path
  - which cephadm
    
# install ceph services all nodes.
  - yum update -y 
  - yum install cephadm ceph-mon ceph-osd ceph-mgr ceph-common -y
# Update kernel for centos 7
  - rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
  - rpm -Uvh https://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
  - yum list available --disablerepo='*' --enablerepo=elrepo-kernel
  # install the latest mainline kernel
  - sudo yum --enablerepo=elrepo-kernel install kernel-ml
  # Set Default Kernel Version
  - vi /etc/default/grub
  > GRUB_DEFAULT=0
  - sudo grub2-mkconfig -o /boot/grub2/grub.cfg
  - reboot
  - uname -r
  > 5.7.12-1.el7.elrepo.x86_64
# install sync time chrony
  - yum install chrony -y
  - systemctl start chronyd
  - systemctl enable chronyd
  
# bootstrap the cluster run the following command just the IP for the first cluster node.
  # run this command if have more 1 NIC and config Mon ip later after bootstrap finished.
  - cephadm bootstrap --mon-ip 192.168.1.41 --skip-mon-network
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
# install git all nodes
  - yum install git -y
# Config osd node storage cluster for iscsi
  - ceph tell osd.0 config set osd_heartbeat_grace 20
  - ceph tell osd.0 config set osd_heartbeat_interval 5
  
# Install TCMU-RUNNER
  - git clone https://github.com/open-iscsi/tcmu-runner
  - cd tcmu-runner
  - cmake -Dwith-glfs=false -Dwith-qcow=false -DSUPPORT_SYSTEMD=ON -DCMAKE_INSTALL_PREFIX=/usr
  - make install
  - systemctl daemon-reload
  - systemctl enable tcmu-runner
 
# Install RTSLIB-FB
  - git clone https://github.com/open-iscsi/rtslib-fb.git
  - cd rtslib-fb
  - python setup.py install

# Configshell-fb
  - git clone https://github.com/open-iscsi/configshell-fb.git
  - cd configshell-fb
  - python setup.py install
  
# Install targetcli-fb
  - git clone https://github.com/open-iscsi/targetcli-fb.git
  - cd targetcli-fb
  - python setup.py install
  - mkdir /etc/target
  - mkdir /var/target
  
# Install ceph-iscsi
  - git clone https://github.com/ceph/ceph-iscsi.git
  - cd ceph-iscsi
  - python setup.py install --install-scripts=/usr/bin
  - cp usr/lib/systemd/system/rbd-target-gw.service /lib/systemd/system
  - cp usr/lib/systemd/system/rbd-target-api.service /lib/systemd/system
  - systemctl daemon-reload
  - systemctl enable rbd-target-gw
  - systemctl start rbd-target-gw
  - systemctl enable rbd-target-api
  - systemctl start rbd-target-api
  
