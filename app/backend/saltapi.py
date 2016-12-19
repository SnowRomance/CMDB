# -*- coding: utf-8 -*-

import urllib2,urllib
import re

try:
    import json
except ImportError:
    import simplejson as json

class SaltAPI(object):
    __token_id = ''
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password

    def token_id(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        content = self.postRequest(obj,prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def get_token_id(self):
        return self.__token_id

    def postRequest(self,obj,prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token'   : self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions,minions_pre

    def delete_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def remote_noarg_execution(self,tgt,fun):
        ''' Execute commands without parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

    def remote_execution(self,tgt,fun, args):
        ''' Command execution with parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        for k,v in args.iteritems():
            params[k] = v
        obj = urllib.urlencode(params)
        obj, number = re.subn("arg\d", 'arg', obj)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return']
        return ret
#       return content['return'][0]['shikee_web001']

    def target_remote_execution(self,tgt,fun,arg):
        ''' Use targeting for remote execution '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def deploy(self,tgt,arg):
        ''' Module deployment '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        return content

    def async_deploy(self,tgt,arg):
        ''' Asynchronously send a command to connected minions '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def target_deploy(self,tgt,arg):
        ''' Based on the node group forms deployment '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid


def main():
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    sapi = SaltAPI(url='https://120.76.130.53:8888',username='salt',password='salt')
    # sapi.token_id()
    #print sapi.list_all_key()
    #sapi.delete_key('test-01')
    #sapi.accept_key('test-01')
    #sapi.deploy('test-01','nginx')
    # print sapi.remote_noarg_execution('iZ940kub0iuZ','test.ping')
    # print sapi.remote_execution('iZ940kub0iuZ','user.chshell', '')
    # print sapi.remote_noarg_execution('iZ940kub0iuZ','ssh.user_keys')
    # print sapi.remote_execution('iZ940kub0iuZ','user.add', {'arg1':'yangjunliu'})
    # print sapi.remote_execution('iZ940kub0iuZ','cmd.run',{'arg1':"ssh-keygen -t dsa -P '' -f /home/yangjunliu/.ssh/id_rsa", 'arg2': 'runas=yangjunliu'})
    # print sapi.remote_execution('iZ940kub0iuZ', 'cmd.run', {'arg1': 'cp /home/yangjunliu/.ssh/id_rsa.pub /home/yangjunliu/.ssh/authorized_keys', 'arg2':'runas=yangjunliu'})

    # print sapi.remote_execution('120.76.130.53', 'cmd.run', {'arg1': "mv /var/cache/salt/master/minions/iZ940kub0iuZ/files/home/yangjunliu/.ssh/id_rsa /web/CMDB/static/upload/yangjunliu_cmdb_login_id_rsa"})
    accepet_keys = sapi.list_all_key()
    print accepet_keys[0]
    for ac_key in accepet_keys[0]:
        content = sapi.remote_noarg_execution(ac_key, 'grains.items')
        print content['id']
        print content['ip_interfaces']

if __name__ == '__main__':
    main()
