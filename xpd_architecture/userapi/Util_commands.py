'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'

from xpd_architecture.dataapi.Utils.Gas_Valve import *
from xpd_architecture.dataapi.Utils.Counts import *
import cothread
from cothread.catools import *
from xpd_architecture.dataapi.config._conf import _conf
import time

def Gas(new_gas=None):
    """
    Returns the current gas name, or sets the new gas
    :param new_gas: New Gas name
    :type new_gas: str
    :return: Gas name
    :rtype: str
    """
    if new_gas is None:
        cur_pos=gas_position()
        for gas, valvepos in valve_asg.items():
            if valvepos==cur_pos:
                print gas
                return gas
    elif valve_asg.has_key(new_gas):
        gas_position(valve_asg[new_gas])
        return Gas()
    else:
        print '%s is not a recognised gas, please change gas configuration.' % (new_gas,)