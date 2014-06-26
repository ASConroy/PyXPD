__author__ = 'Christopher J. Wright'

from cothread.catools import *
from decimal import *
from pyXPD.instrumentapi.config._conf import _conf, __initPV


# this is used later on for the determination if moves are in resolution
getcontext().prec = 8

# read configuration file motor section, and test their connection
pv_fail, pv_pass = __initPV(section='Motor PVs')

# create motor dictionary, which will hold information about the motors
motorD = dict()
# loop loads up the pv information for the pvs that pass the connection test
for option in pv_pass:
    pv = _conf.get('Motor PVs', option)
    motorD[option] = {'pv': pv, 'low': caget(pv + '.LLM'), 'high': caget(pv + '.HLM'), 'EGU': caget(pv + '.EGU'),
                      'res': caget(pv + '.MRES')}


def move(alias=None, value=None, wait=False, printop=False):
    # check final position within limits
    motor = motorD[alias]
    # print motorD
    if motor['low'] <= value <= motor['high']:
        # check is move is within motor resolution,
        if abs(Decimal(value).remainder_near(Decimal(motor['res']))) < 1e-10:
            caput(motor['pv'], value, wait=wait, timeout=None)
        else:
            raise Exception('Move specified with more precision than instrument allows')
    else:
        raise Exception('Out of Bounds, the soft limit has been reached')


def rmove(alias=None, value=None, wait=False, printop=False):
    absvalue = value + position(alias)
    move(alias, absvalue, wait=False, printop=False)


def position(alias=None, **kwargs):
    if kwargs == {}:
        motor = motorD[alias]
        pos = caget(motor['pv'] + '.DRBV')
        return float(pos)
        # other posibilities


def resolution(**kwargs):
    if kwargs == {}:
        print('Current resolutions for the motors are:\n')
        for element in motorD:
            print 'Motor: %s, Resolution: %s' % (element, element['res'])
    else:
        for key in kwargs.keys():
            print motorD[key]['res']


def multi_move(movedict=None):
    multiD = {}
    for key, value in movedict.items():
        motor = motorD[key]
        if motor['low'] <= value <= motor['high']:
            if abs(Decimal(value).remainder_near(Decimal(motor['res']))) < 1e-10:
                multiD[motor['pv']] = value
            else:
                raise Exception('Move specified with more precision than instrument allows')
        else:
            raise Exception('Out of Bounds, the soft limit has been reached')

    for key, value in multiD.items():
        # print 'HI'
        caput(key, value, wait=False)
    # print 'Stuff'
    finished = 0
    while finished == 0:
        # print finished
        finished = 1
        for key in multiD.keys():
            # print caget(key+'.DMOV')
            finished *= caget(key + '.DMOV')
