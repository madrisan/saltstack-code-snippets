# -*- coding: utf-8 -*-
'''
Module for managing users and groups

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''

# Import salt libs
import salt.utils

__virtualname__ = 'account'

def get_group_list():
    '''
    Return the list of the groups configured in /etc/group

    CLI Example:

        .. code-block:: bash

            salt '*' account.get_group_list

    '''
    file_group = '/etc/group'

    def secgroups(infos):
        groups = infos[3].strip()
        return groups.split(',') if len(groups) > 0 else ''

    group_infos = []
    with salt.utils.fopen(file_group, 'r') as fp_:
        group_infos = [line.split(':') for line in fp_]

    return dict(
        [(infos[0], {
            'gid': infos[2],
            'secgroups': secgroups(infos)
        }) for infos in group_infos])
