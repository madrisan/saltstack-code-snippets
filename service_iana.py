# -*- coding: utf-8 -*-
'''
SaltStack code snippets.
Module for managing IANA services (/etc/services).
Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''
# Import python libs
import collections
import os

# Import salt libs
import salt.utils
from salt.exceptions import CommandExecutionError

# Define the module's virtual name
__virtualname__ = 'service_iana'

file_services = '/etc/services'

def __virtual__():
    if not os.path.exists(file_services):
        return (False, 'The {0} file cannot be found.'.format(file_services))
    return True

def get_service_list():
    '''
    Return the list of the services configured in /etc/services

    CLI Example:

        .. code-block:: bash

            salt '*' service_iana.get_service_list

    '''
    toks = ('name', 'port')
    Service = collections.namedtuple('Service', toks)
    skip_line = lambda line: line.lstrip().startswith('#') or not line.strip()

    service_infos = []
    try:
        with salt.utils.fopen(file_services, 'r') as fp_:
            # just take the first two tokens and ignore the comment (if any)
            service_infos = [Service(*line.split()[:2]) for line in fp_
                if not skip_line(line)]
    except:
        raise CommandExecutionError(
            'An error has occurred while reading {0} at line\n{1}'.format(
                file_services, line)
        )

    return dict([
        (service.port, {
            'name': service.name,
            'port': service.port.split('/')[0],
            'protocol': service.port.split('/')[1]
        }) for service in service_infos])
