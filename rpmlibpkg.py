# -*- coding: utf-8 -*-
'''
SaltStack code snippets.
Module for querying informations from the rpm database.
This module make use of the rpm python bindings.
Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''
# Import python libs
import time

try:
    import rpm
    HAS_RPM_LIBS = True
except ImportError:
    HAS_RPM_LIBS = False

# Define the module's virtual name
__virtualname__ = 'rpmlibpkg'

def __virtual__():
    if __grains__.get('os_family') == 'RedHat':
        if not HAS_RPM_LIBS:
            return (False, 'The rpm python library cannot be loaded')
        return True

    return (False,
        'The {0} module cannot be loaded: '
        'unsupported OS family'.format(__virtualname__))

def list_pkgs():
    '''
    List the packages currently installed in a dict::

        {'<package_name>': '<epoch>:<version>-<release>.<arch>'}

    CLI Example:

        .. code-block:: bash

            salt '*' rpmlibpkg.list_pkgs
    '''
    ts = rpm.TransactionSet()
    mi = ts.dbMatch()
    epoch = lambda h: "%s:" % h['epoch'] if h['epoch'] else ''
    pkgs = dict([
        (h['name'], "%s%s-%s.%s" % (
            epoch(h), h['version'], h['release'], h['arch']))
        for h in mi])
    return pkgs

def lastupdate():
    '''
    Return the date of the last rpm package update/installation.

    CLI Example:

        .. code-block:: bash

            salt '*' rpmlibpkg.lastupdate
    '''
    installdate = lambda h: h.sprintf("%{INSTALLTID:date}")
    installptime = lambda h: time.strptime(installdate(h), "%c")

    ts = rpm.TransactionSet()
    mi = ts.dbMatch()
    last = max(installptime(h) for h in mi)

    return time.asctime(last)

def buildtime():
    '''
    Return the build date and time.

    CLI Example:

        .. code-block:: bash

            salt '*' rpmlibpkg.buildtime
    '''
    installdate = lambda h: h.sprintf("%{INSTALLTID:date}")
    installptime = lambda h: time.strptime(installdate(h), "%c")

    ts = rpm.TransactionSet()
    mi = ts.dbMatch()
    first = min(installptime(h) for h in mi)

    return time.asctime(first)
