#/usr/bin/python
# -*- coding: utf-8 -*-

import salt.client




class saltapi():
    def getclient(self):
        return salt.client.LocalClient()
    
    
    def execute(self,tgt,fun,args):
        loc=salt.client.LocalClient()
        re=loc.cmd_async(tgt,fun,[args])
        
        
if __name__ == '__main__':
    pass