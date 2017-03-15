#!/usr/bin/python
# Check for system configuration issues on a Red Hat cluster
# Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

from __future__ import print_function

__author__ = "Davide Madrisan"
__copyright__ = "Copyright 2017 Davide Madrisan"
__license__ = "GPL"
__version__ = "1"
__email__ = "davide.madrisan.gmail.com"
__status__ = "Beta"

# Import python libs
import getopt
import itertools
import os
import sys

# Import salt libs
import salt.client.ssh.client

try:
    import json
except ImportError:
    import simplejson as json

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
        'Check for system configuration issues on a Red Hat cluster',
        'Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>',
        'Usage:',
        '\t' + progname + ' --cluster <hostnames>',
        '\t' + progname + ' -h',
        'Example:\n' + '\tsudo %s -c "cluster01,cluster02"' % progname ]:
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

def checkup(ssh_client, cluster_hostnames):
    checks = [('groups', 'account.get_group_list'),
        ('users', 'account.get_user_list'),
        ('services', 'service_iana.get_service_list')]

    def get_objs(ssh_client, target, salt_module):
        '''
        Return the system objects locally configured on target
        '''
        return saltstack_module_run(
            ssh_client, target, salt_module)

    def print_deviations(text, target, deviations):
        print('{0}: {1}:{2}'.format(target, text,
              ' OK' if not deviations else
              ''.join(['\n - ' + dev for dev in sorted(deviations)])))

    for check, salt_module in checks:
        print('*** Checking {0}'.format(check))
        objs_per_host = dict(
            (target, get_objs(ssh_client, target, salt_module))
                for target in cluster_hostnames)
        all_objs = set(itertools.chain(*[
            objs_per_host.get(target).keys() for target in cluster_hostnames]))

        for target in cluster_hostnames:
            target_objs = set(objs_per_host.get(target).keys())
            missing = all_objs.difference(target_objs)
            print_deviations('missing {0}'.format(check), target, missing)

def get_items(target, infos, query):
    j = json.loads(json.dumps(infos))
    return dict(
        [(q, j.get(target, {}).get('return', {}).get(q, "")) for q in query])

def get_salt_grains(ssh_client, target):
    '''
    Return all the grains provided by SaltStack for the host 'target'
    '''
    # returns one item per target (host)
    return ssh_client.cmd_iter(target, 'grains.items')

def main(cluster_hostnames):
    ssh_client = salt.client.ssh.client.SSHClient()
    grains = dict()
    for target in cluster_hostnames:
        for infos in get_salt_grains(ssh_client, target):
            # NOTE: dump all the grabbed data just fot debugging
            #print(json.dumps(infos, sort_keys=True, indent=2, separators=(',', ': ')))
            grains = get_items(target, infos, (
                'osarch',
                'osfullname',
                'osrelease_info'))

        os_version = '.'.join(str(n) for n in grains['osrelease_info'])
        os = "{0} {1}".format(grains['osfullname'], os_version)
        osarch = grains['osarch']

        is_cluster, cluster_tech = saltstack_module_run(
            ssh_client, target,'cluster.is_active')
        if not is_cluster:
            die('{0}: Not a cluster node'.format(target))

        print("{0}:\n - os: {1} ({2})\n - cluster tecnology: {3}".format(
            target, os, osarch, cluster_tech))

    checkup(ssh_client, cluster_hostnames)

if __name__ == '__main__':
    cluster_hostnames = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:h',
            ["cluster=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--cluster'):
            cluster_hostnames = a.strip().split(',')
        else:
            assert False, 'unhandled option'

    if not cluster_hostnames: usage(); sys.exit(2)
    if os.geteuid() != 0:
        die('This script must be run as root')

    try:
        main(cluster_hostnames)
    except KeyboardInterrupt:
        die(3, 'Exiting on user request')
    sys.exit(0)
