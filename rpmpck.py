# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Get the date of the last rpm package update/installation

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''

# Import python libs
import time

try:
    import rpm
    HAS_RPM_LIBS = True
except ImportError:
    HAS_RPM_LIBS = False

___virtualname__ = 'rpmpck'

def __virtual__():
    if __grains__.get('os_family') == 'RedHat':
        if not HAS_RPM_LIBS:
            return (False, 'The rpm python lib cannot be loaded')
        return __virtualname__

    return (False,
        'The {0} module cannot be loaded: '
        'unsupported OS family'.format(__virtualname__))

def lastupdate():
    '''
    Return the date of the last rpm package update/installation.

    CLI Example:

        .. code-block:: bash

            salt '*' rpmpck.lastupdate
    '''
    installdate = lambda h: h.sprintf("%{INSTALLTID:date}")
    installptime = lambda h: time.strptime(installdate(h), "%c")

    ts = rpm.TransactionSet()
    mi = ts.dbMatch()
    latest = max(installptime(h) for h in mi)

    return time.asctime(latest)
