#!/usr/bin/env python
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("E://Py_Work/CMDB/app/backend/config.ini")
def dbconfig():
    db_host = cf.get("db","db_host")
    db_port = cf.get("db","db_port")
    db_user = cf.get("db","db_user")
    db_pass = cf.get("db","db_pass")
    db_name = cf.get("db","db_name")
    db = {"host":db_host,"port":db_port,"user":db_user,"pass":db_pass,"name":db_name}
    return db

def saltconfig():
    salt_url = cf.get("saltstack", "url")
    salt_user = cf.get("saltstack", "user")
    salt_pass = cf.get("saltstack", "pass")
    salt_ip = cf.get("saltstack", "salt_ip")
    salt_master_name = cf.get("saltstack", "salt_master_name")
    salt = {"salt_url": salt_url, "salt_user": salt_user, "salt_pass": salt_pass, "salt_ip": salt_ip, "salt_master_name": salt_master_name}
    return salt