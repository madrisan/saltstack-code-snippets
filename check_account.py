#!/usr/bin/python
# Check for system configuration issues on a Red Hat cluster
# Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

from __future__ import print_function

__author__ = "Davide Madrisan"
__copyright__ = "Copyright 2017 Davide Madrisan"
__license__ = "GPL"
__version__ = "1"
__email__ = "davide.madrisan@gmail.com"
__status__ = "Beta"

# Import python libs
import getopt
import os
import sys
from collections import namedtuple

# Import salt libs
import salt.client.ssh.client
import salt.utils
from salt.exceptions import CommandExecutionError

def die(message, exitcode=1):
    '''
    Print an error message and exit with the given 'exitcode'
    '''
    progname = sys.argv[0]
    print('{0}: error: {1}'.format(progname, message), file=sys.stderr)
    sys.exit(exitcode)

def usage():
    progname = sys.argv[0]
    for line in [
        'Check users and groups configuration',
        'Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>',
        'Usage:',
        '\t' + progname + ' --user <user>[,<user2>,...] <hostame>',
        '\t' + progname + ' -h',
        'Example:\n' + '\tsudo %s -u hyperic frsopslapp052' % progname ]:
        print(line)

def saltstack_module_run(ssh_client, target, modulename, params=None):
    '''
    Return the 'return' entry of the dict returned by SaltStack
    '''
    saltstack_get_obj = lambda data, obj: data.get(target, {}).get(obj, {})
    json_out = (
        ssh_client.cmd(target, modulename, params) if params
            else ssh_client.cmd(target, modulename))
    errmsg = saltstack_get_obj(json_out, 'stderr')
    outmsg = saltstack_get_obj(json_out, 'stdout')
    if errmsg:
        die('probably a BUG...\n{0} {1}'.format(errmsg, outmsg))

    return saltstack_get_obj(json_out, 'return')

def get_users_infos(ssh_client, target, users):
    '''
    Return a dictionary containing the system informations for
    the list of users 'users'.
    '''
    all_groups = saltstack_module_run(
        ssh_client, target, 'account.get_group_list')
    group_names = all_groups.keys()

    def _pack_data(user):
        data = saltstack_module_run(
            ssh_client, target, 'user.info', [user])
        if not data:
            raise CommandExecutionError(
                'Unable to find the user: {0}'.format(user))
        gid = data['gid']
        groups = [grp for grp in group_names if all_groups[grp]['gid'] == gid]
        secgroups = [grp for grp in data['groups'] if grp not in groups]

        return dict(
            group = ','.join(groups),
            shell = data['shell'],
            home = data['home'],
            secgroups = ','.join(secgroups),
        )

    return dict((user, _pack_data(user)) for user in users)

def print_user_info(user, data, raw):
    '''
    Print the informations of the user 'user' and its raw
    line entry in /etc/passwd

    Example of output:

        [user oracle]
              group: oinstall
               home: /home/oracle
          secgroups: asmdba,dba,oper,sysbackup
              shell: /bin/bash
           raw line: oracle:500:501::/home/oracle:/bin/bash
    '''
    print('[user {0}]'.format(user))
    items = sorted(data.keys())
    for item in items:
        print('{0:>15}: {1}'.format(item, data.get(item)))
    print('{0:>15}: {1}'.format('raw line', raw))

def get_passwd_data(ssh_client, target):
    '''
    Return a dictionary containing the data found in the file /etc/passwd.
    (key = username, value = the raw line of the corresponding user)
    '''
    tokens = ('username', 'passwd', 'uid', 'gid', 'gecos', 'homedir', 'shell')
    User = namedtuple('User', tokens)
    try:
        passwd_raw = saltstack_module_run(
            ssh_client, target, 'account.get_passwd_raw')
        user_infos = list(User(*line.rstrip().split(':'))
            for line in passwd_raw)
    except:
        raise CommandExecutionError(
            'An error has occurred while reading {0}'.format(filename)
        )
    def _pack_data(user):
        return '{0}:{1}:{2}:{3}:{4}:{5}'.format(
            user.username,
            user.uid,
            user.gid,
            user.gecos,
            user.homedir,
            user.shell)
    return dict((user.username, _pack_data(user)) for user in user_infos)

def main(target, users):
    ssh_client = salt.client.ssh.client.SSHClient()
    out = get_users_infos(ssh_client, target, users)
    passwd = get_passwd_data(ssh_client, target)
    for user in users:
        print_user_info(user, out.get(user), passwd.get(user))

if __name__ == '__main__':
    hostname, users = (None, None)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:h',
            ["user=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-u', '--user'):
            users = a.strip().split(',')
        else:
            die('Unhandled command line option: {0}'.format(o))

    if not users or len(args) != 1: usage(); sys.exit(2)
    if os.geteuid() != 0:
        die('This script must be run as root')

    target = args[0]
    try:
        main(target, users)
    except KeyboardInterrupt:
        die(3, 'Exiting on user request')
    sys.exit(0)
