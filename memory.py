# -*- coding: utf-8 -*-
'''
SaltStack code snippets
This module is a simple wrapper to status.meminfo

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''

# Define the module's virtual name
__virtualname__ = 'memory'

def _sizeof_fmt(tok, factor=1024.0, skip=1, suffix='B'):
    '''
    Divide 'tok' to its best unit and append it to the output.
    '''
    try:
        num = int(tok)
    except ValueError:
        return tok

    units = ['', 'k','M','G','T','P']
    for unit in units[skip:]:
        if num < factor:
            return "%3.0f %s%s" % (num, unit, suffix)
        num /= factor
    return "%.0f %s%s" % (num, 'p', suffix)

def usage(human_readable=True):
    '''
    Return some informations on physical memory and swap

    CLI Example:

    .. code-block:: bash

        salt '*' memory.usage
    '''
    fmt = lambda num: _sizeof_fmt(num) if human_readable else num

    mem_infos = __salt__['status.meminfo']()
    getvalue = lambda memtype: fmt(mem_infos.get(memtype, {}).get('value', 0))

    memtypes = ['MemFree', 'MemTotal', 'SwapFree', 'SwapTotal']
    infos = dict((memtype, getvalue(memtype)) for memtype in memtypes)

    try:
        infos['MemAvailable'] = getvalue('MemAvailable')
    except:
        pass

    return infos
