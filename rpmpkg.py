# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Module for querying informations from the rpm database.

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''

# Import python libs
import time

# Import salt libs
import salt.utils.itertools

__virtualname__ = 'rpmpkg'

def __virtual__():
    '''
    Confine this execution module to rpm based systems
    '''
    if not salt.utils.which('rpm'):
        return (False, 'The rpm binary is not in the path.')
    return True

def list_pkgs(*packages):
    '''
    List the packages currently installed in a dict::

        {'<package_name>': '<epoch>:<version>-<release>.<arch>'}

    '''
    pkgs = {}
    cmd = ['rpm', '-q' if packages else '-qa', '--queryformat',
           r'%{NAME} %|EPOCH?{%{EPOCH}}:{0}|:%{VERSION}-%{RELEASE}.%{ARCH}\n']

    if packages:
        cmd.extend(packages)
    out = __salt__['cmd.run'](cmd, output_loglevel='trace',
                              python_shell=False)
    for line in salt.utils.itertools.split(out, '\n'):
        if 'is not installed' in line:
            continue
        comps = line.split()
        pkgs[comps[0]] = comps[1]

    return pkgs

def lastupdate():
    '''
    Return the date of the last rpm package update/installation.

    CLI Example:

        .. code-block:: bash

            salt '*' rpmpck.lastupdate
    '''
    installtime = lambda rpm_date: time.strptime(rpm_date, "%c")

    cmd = ['rpm', '-qa', '--queryformat', r'%{INSTALLTID:date}\n']
    out = __salt__['cmd.run'](cmd, output_loglevel='trace',
                              python_shell=False).splitlines()
    last = max(installtime(rpm_date) for rpm_date in out)

    return time.asctime(last)

def buildtime():
    '''
    Return the build date and time.

    CLI Example:

        .. code-block:: bash

            salt '*' rpmpck.buildtime
    '''
    installtime = lambda rpm_date: time.strptime(rpm_date, "%c")

    cmd = ['rpm', '-qa', '--queryformat', r'%{INSTALLTID:date}\n']
    out = __salt__['cmd.run'](cmd, output_loglevel='trace',
                              python_shell=False).splitlines()

    first = min(installtime(rpm_date) for rpm_date in out)

    return time.asctime(first)
