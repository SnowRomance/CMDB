#!/bin/bash
####install epel_yum######
yum install epel-release -y
####yum install client#####
yum install salt-minion -y
#####change config####
#####sh install_server.sh server_ip#####
sed -i "s/#master: salt/master: $1/g" /etc/salt/minion
#####start master####
service salt-minion start
