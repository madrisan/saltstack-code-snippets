# -*- coding: utf-8 -*-
'''
SaltStack code snippets.
Module for managing users and groups.
Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''
# Import python libs
from collections import namedtuple 

# Import salt libs
import salt.utils
from salt.exceptions import CommandExecutionError

# Define the module's virtual name
__virtualname__ = 'account'

def get_group_list():
    '''
    Return the list of the groups configured in /etc/group

    CLI Example:

        .. code-block:: bash

            salt '*' account.get_group_list
    '''
    file_group = '/etc/group'
    tokens = ('groupname', 'passwd', 'gid', 'grouplist')
    Group = namedtuple('Group', tokens)
    try:
        with salt.utils.fopen(file_group, 'r') as fp_:
            group_infos = list(Group(*line.split(':')) for line in fp_)
    except:
        raise CommandExecutionError(
            'An error has occurred while reading {0}'.format(file_group)
        )

    def _secondary_groups(group):
        grouplist = group.grouplist.strip()
        return grouplist.split(',') if len(grouplist) > 0 else ''
    def _pack_data(group):
        secgroups = _secondary_groups(group)
        return dict(
            gid = int(group.gid), grouplist = secgroups
        ) if secgroups else dict(gid = int(group.gid))
    return dict((group.groupname, _pack_data(group)) for group in group_infos)

def get_user_list():
    '''
    Return the list of the users configured in /etc/passwd

    CLI Example:

        .. code-block:: bash

            salt '*' account.get_user_list
    '''
    file_user = '/etc/passwd'
    tokens = ('username', 'passwd', 'uid', 'gid', 'gecos', 'homedir', 'shell')
    User = namedtuple('User', tokens)
    try:
        with salt.utils.fopen(file_user, 'r') as fp_:
            user_infos = list(User(*line.rstrip().split(':')) for line in fp_)
    except:
        raise CommandExecutionError(
            'An error has occurred while reading {0}'.format(file_user)
        )

    def _pack_data(user):
        return dict(
            uid = int(user.uid),
            gid = int(user.gid),
            gecos = user.gecos,
            homedir = user.homedir,
            shell = user.shell)
    return dict((user.username, _pack_data(user)) for user in user_infos)
