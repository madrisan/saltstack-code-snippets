# -*- coding: utf-8 -*-
'''
Module for managing the Pacemaker clusters
Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''

# Import python libs
from xml.dom.minidom import parseString
try:
    from pcs import (
        resource,
        utils,
    )
    from pcs.lib import pacemaker as lib_pacemaker
    HAS_PCS_LIBS = True
except ImportError:
    HAS_PCS_LIBS = False

# Import salt libs
from salt.exceptions import CommandExecutionError

# Define the module's virtual name
__virtualname__ = 'pacemaker'

def __virtual__():
    '''
    Confine this execution module on Red Hat systems with the pcs library
    '''
    if __grains__.get('os_family') == 'RedHat':
        if not HAS_PCS_LIBS:
            return (False, 'The pcs python library cannot be loaded')
        return True

    return (False,
        'The {0} module cannot be loaded: '
        'unsupported OS family'.format(__virtualname__))

def cluster_local_node():
    '''
    Return the name of the local cluster member.

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.cluster_local_node
    '''
    node_status = cluster_local_node_status()
    return node_status.get('name', '')

def cluster_local_node_status():
    '''
    Return the status of the local cluster member.

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.cluster_local_node_status
    '''
    try:
        node_status = lib_pacemaker.get_local_node_status(
            utils.cmd_runner()
        )
    except LibraryError as e:
        raise CommandExecutionError('Unable to get node status: {0}'.format(
            '\n'.join([item.message for item in e.args]))
        )
    return node_status

def cluster_name():
    '''
    Return the cluster name.

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.cluster_name
    '''
    return utils.getClusterName()

_get_node_attr = lambda node, attr: node.getAttribute(attr)

def _get_all_nodes():
    info_dom = utils.getClusterState()
    nodes = info_dom.getElementsByTagName('nodes')
    if nodes.length == 0:
        raise CommandExecutionError('No nodes section found')
    all_nodes = nodes[0].getElementsByTagName('node')
    return all_nodes

def cluster_nodes():
    '''
    Return the list of cluster nodes.

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.cluster_nodes
    '''
    all_nodes = _get_all_nodes()
    name = lambda node: _get_node_attr(node, 'name')
    return list(name(node) for node in all_nodes)

def cluster_nodes_status():
    name = lambda node: _get_node_attr(node, 'name')
    maintenance = lambda node: _get_node_attr(node, 'maintenance') == 'true'
    online = lambda node: _get_node_attr(node, 'online') == 'true'
    # FIXME: remote nodes are not supported (see: pcs/status.py):
    #remote = lambda node: _get_node_attr(node, 'type') == 'remote'
    standby = lambda node: _get_node_attr(node, 'standby') == 'true'

    all_nodes = _get_all_nodes()
    maintenancenodes = list(
        name(node) for node in all_nodes if maintenance(node))
    onlinenodes = list(name(node) for node in all_nodes if online(node))
    offlinenodes = list(
        name(node) for node in all_nodes if name(node) not in onlinenodes)
    standbynodes = list(name(node) for node in all_nodes if standby(node))

    return dict(
        maintenancenodes = maintenancenodes,
        offlinenodes = offlinenodes,
        onlinenodes = onlinenodes,
        standbynodes = standbynodes)

def cluster_resource_group_list():
    groups = list()
    group_xpath = '//group'
    group_xml = utils.get_cib_xpath(group_xpath)
    # If no groups exist, we silently return
    if not group_xml:
        return groups

    element = parseString(group_xml).documentElement
    # If there is more than one group returned it's wrapped in an xpath-query
    # element
    elements = (element.getElementsByTagName('group')
        if element.tagName == 'xpath-query' else list(element))
    return dict((e.getAttribute("id"),
                 list(e.getAttribute("id") for e in
                     e.getElementsByTagName("primitive"))) for e in elements)

def cluster_resources():
    '''
    Return the cluster status resources.

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.cluster_resources
    '''
    info_dom = utils.getClusterState()
    resources = info_dom.getElementsByTagName('resources')
    if resources.length == 0:
        raise CommandExecutionError('No resources section found')

    def _pack_data(resource):
        nodes = resource.getElementsByTagName('node')
        node = list(node.getAttribute('name')
                   for node in nodes if nodes.length > 0)
        resource_agent = resource.getAttribute('resource_agent')
        resource_id = resource.getAttribute('id')
        role = resource.getAttribute('role')
        return (resource_id, dict(
                resource_agent = resource_agent,
                role = role,
                node = node[0] if len(node) == 1 else node))

    return dict(_pack_data(resource)
        for resource in resources[0].getElementsByTagName('resource'))

def cluster_service_status():
    '''
    Return the status (enable/running) of the cluster services?

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.cluster_service_status
    '''
    services = [
        'corosync',
        'pacemaker',
        'pacemaker_remote',
        'pcsd',
        'sbd',
    ]
    enabled_services = __salt__['service.get_enabled']()
    def _pack_data(service):
        enabled = service in enabled_services
        running = __salt__['service.status'](service)
        return dict(
            enabled = enabled,
            running = running,
        )
    return dict((service, _pack_data(service)) for service in services)

def cluster_stonith_configured():
    '''
    Check whether stonith is configured or not.
    Return False if no stonith devices are detected and
    stonith-enabled is not false.

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.cluster_stonith_configured
    '''
    return not utils.stonithCheck()

def is_cluster_member():
    '''
    Check if a system cluster is running on this node.

    CLI Example:

        .. code-block:: bash

            salt '*' pacemaker.is_cluster_member
    '''
    monitor_command = ['crm_mon', '--one-shot']
    output, retval = utils.run(monitor_command)
    if retval != 0:
        return (False, 'Cluster is not currently running on this node')
    return (True)
