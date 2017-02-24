# -*- coding: utf-8 -*-
'''
SaltStack code snippets.
Module for managing users and groups.
Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''
# Import python libs
import collections

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
    toks = ('groupname', 'passwd', 'gid', 'grouplist')
    Group = collections.namedtuple('Group', toks)

    def secgroups(group):
        grouplist = group.grouplist.strip()
        return grouplist.split(',') if len(grouplist) > 0 else ''

    group_infos = []
    try:
        with salt.utils.fopen(file_group, 'r') as fp_:
            group_infos = [Group(*line.split(':')) for line in fp_]
    except:
        raise CommandExecutionError(
            'An error has occurred while reading {0}'.format(file_group)
        )
    return dict(
        [(group.groupname, {
            'gid': group.gid,
            'grouplist': secgroups(group)
        }) for group in group_infos])

def get_user_list():
    '''
    Return the list of the users configured in /etc/passwd

    CLI Example:

        .. code-block:: bash

            salt '*' account.get_user_list

    '''
    file_user = '/etc/passwd'
    toks = ('username', 'passwd', 'uid', 'gid', 'gecos', 'homedir', 'shell')
    User = collections.namedtuple('User', toks)

    user_infos = []
    try:
        with salt.utils.fopen(file_user, 'r') as fp_:
            user_infos = [User(*line.rstrip().split(':')) for line in fp_]
    except:
        raise CommandExecutionError(
            'An error has occurred while reading {0}'.format(file_user)
        )
    return dict(
        [(user.username, {
            'uid': user.uid,
            'gid': user.gid,
            'gecos': user.gecos,
            'homedir': user.homedir,
            'shell': user.shell
        }) for user in user_infos])
