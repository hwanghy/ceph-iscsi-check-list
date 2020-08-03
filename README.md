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
  > 10.0.0.2 ceph2
  > 10.0.0.3 ceph3

# Stop firewalld all nodes
- systemctl stop firewalld

# Disable selinux
- vi /etc/selinux/config
  > SELINUX=disabled
> reboot

# make cephadm folder
  > mkdir cephadm
  > mkdir /etc/ceph
  > cd cephadm

# Install docker all nodes
