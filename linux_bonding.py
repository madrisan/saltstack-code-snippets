# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Check the network bonding topology.

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''
# Import 3rd-party libs
import os

# Import salt libs
import salt.utils

__virtualname__ = 'linux_bonding'
proc_net_bonding = '/proc/net/bonding'

def __virtual__():
    '''
    Only run on Linux systems
    '''
    if __grains__['kernel'] != 'Linux':
        return (False, 'The {0} execution module cannot be loaded: '
                       'only available on Linux systems.'.format(
                       __virtualname__))
    return True

def _get_proc_bonding_files():
    bonding_interface_paths = __salt__['file.find'](
        proc_net_bonding,
        mindepth=1,
        maxdepth=1
    )
    return bonding_interface_paths

def _parse_proc_bond_file(procfile):
    data = dict()
    slave_interface = None
    slave_interfaces = list()
    with salt.utils.fopen(procfile, 'r') as fp_:
        for descr, value in [elm.split(':', 1) for elm in fp_ if elm.strip()]:
            key = descr.strip().lower().replace(' ', '_')
            if key == 'slave_interface':
                slave_interface = value.strip()
                slave_interfaces.append(slave_interface)
            elif slave_interface:
                data.setdefault(slave_interface,{}).update({key: value.strip()})
            else:
                data[key] = value.strip()
        data['slave_interfaces'] = slave_interfaces
    return data

def device_list():
    '''
    Return the list of the bonding device

    CLI Example:

        .. code-block:: bash

            salt '*' linux_bonding.device_list
    '''
    bonding_interface_paths = _get_proc_bonding_files()
    devices = [os.path.basename(procfile)
        for procfile in bonding_interface_paths]
    return devices

def topology():
    '''
    Return the topology of the network bonding

    CLI Example:

        .. code-block:: bash

            salt '*' linux_bonding.topology
    '''
    bonding_interface_paths = _get_proc_bonding_files()
    infos = dict(
        (os.path.basename(procfile), _parse_proc_bond_file(procfile))
            for procfile in bonding_interface_paths)
    return infos
