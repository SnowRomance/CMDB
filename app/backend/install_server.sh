#!/bin/bash
####install epel_yum######
yum install epel-release -y
####yum install client#####
yum install salt-master -y
#####start master####
service salt-master start
