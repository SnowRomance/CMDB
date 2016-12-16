#!/bin/bash
####install epel_yum######
yum install epel-release -y
####yum install client#####
yum install salt-master -y
#### 设置 salt file_rev  #######
sed -i "s/#file_recv: False/file_recv: True/g" /etc/salt/master
sed -i "s/#file_recv_max_size: 100/file_recv_max_size: 10/g" /etc/salt/master
#####start master####
service salt-master start
