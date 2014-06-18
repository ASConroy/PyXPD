# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:55:39 2014
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright
"""

from cothread.catools import *

def __loadConfig():
    import os.path
    import ConfigParser
    cf=ConfigParser.SafeConfigParser()
    cf.optionxform=str
    cf.read([
        # '/etc/user.conf',
        os.path.expanduser('~/user.conf'),
        'user.conf',
        '/home/xpdlabuser/Spyder_Projects/XPD+_architecture/xpd_architecture/dataapi/config/XPD.conf'
    ])
    return cf
    
_userconf=__loadConfig()