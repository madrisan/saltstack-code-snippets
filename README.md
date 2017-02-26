![](images/saltstack_horizontal_dark.png?raw=true)

# SaltStack code snippets for Linux

A set of code snippets that can be used to build SaltStack [execution modules][saltstackexec].

A Salt execution module is a Python or Cython module placed in a directory called `_modules/` at the root of the Salt fileserver, usually `/srv/salt`.

The [scripts](scripts/) folder contains Python sample scripts that make use of SaltStack as a backend.

### [account](account.py) 

  * __account.get_group_list__ - Return the list of local groups
```bash
myserver:
    ----------
    root:
        ----------
        gid:
            0
    ...
    oinstall:
        ----------
        gid:
            501
        secgroups:
            - oracle
    ...
```

  * __account.get_user_list__ - Return the list of local users
```bash
myserver:
    ----------
    bin:
        ----------
        gecos:
            bin
        gid:
            1
        homedir:
            /bin
        shell:
            /sbin/nologin
        uid:
            1
    ...
```

### [cpuinfo](cpuinfo.py)

  * __cpuinfo.proc__ - Return the number of core, logical, and CPU sockets
```bash
myserver:
    ----------
    cores:
        10
    logicals:
        40
    sockets:
        2
```

### [fsinfo](fsinfo.py)

  * __fsinfo.usage__ - Return some informations about the configured file systems
```bash
myserver:
    ----------
    /:
        ----------
        autofs:
            false
        automount:
            true
        available:
            1.8GB
        device:
            /dev/mapper/rootvg-rootlv
        fstype:
            ext4
        lvm-pvdevice:
            /dev/mapper/mpatha2
        lvm-vgname:
            rootvg
        mountpoint:
            /
        scope:
            Unknown
        size:
            1.9GB
    /sharednfs:
        ----------
        autofs:
            false
        automount:
            true
        available:
            477.1GB
        device:
            nas.domain.eu:/PARTNFS/sharedfolder
        fstype:
            nfs
        mountpoint:
            /sharednfs
        size:
            2.0TB
        used:
            1.5TB
    ...
```
### [linux_bonding](linux_bonding.py)

  * __linux_bonding.device_list__ - Return the list of the bonding device
```bash
myserver:
    ----------
    - bond0
```

  * __linux_bonding.topology__ - Return the topology of the network bonding
```bash
myserver:
    ----------
    bond0:
        ----------
        bonding_mode:
            fault-tolerance (active-backup)
        currently_active_slave:
            em1
        down_delay_(ms):
            100
        em1:
            ----------
            duplex:
                full
            link_failure_count:
                0
            mii_status:
                up
            permanent_hw_addr:
                28:f1:0e:70:23:6e
            slave_queue_id:
                0
            speed:
                10000 Mbps
        em2:
            ----------
            duplex:
                full
            link_failure_count:
                0
            mii_status:
                up
            permanent_hw_addr:
                28:f1:0e:70:23:71
            slave_queue_id:
                0
            speed:
                10000 Mbps
        ethernet_channel_bonding_driver:
            v3.7.1 (April 27, 2011)
        mii_polling_interval_(ms):
            100
        mii_status:
            up
        primary_slave:
            None
        slave_interfaces:
            - em1
            - em2
        up_delay_(ms):
            0
```

### [linux_fiberchannel](linux_fiberchannel.py)

  * linux_fiberchannel.show - View system fiber channel device information
```bash
myserver:
    host11:
        ----------
        Class:
            fc_host
        Class Device:
            host11
        Class Device path:
            /sys/devices/virtual/net/em1.550/ctlr_0/host11/fc_host/host11
        Device:
            host11
        Device path:
            /sys/devices/virtual/net/em1.550/ctlr_0/host11
        active_fc4s:
            0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
        dev_loss_tmo:
            60
        fabric_name:
            0x2226000573d92e21
        issue_lip:
            <store method only>
        max_npiv_vports:
            65535
        maxframe_size:
            2048 bytes
        node_name:
            0x200028f10e702370
        npiv_vports_inuse:
            0
        port_id:
            0x6a0801
        port_name:
            0x200128f10e702370
        port_state:
            Online
        port_type:
            NPort (fabric via point-to-point)
        speed:
            10 Gbit
        supported_classes:
            Class 3
        supported_fc4s:
            0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
        supported_speeds:
            1 Gbit, 10 Gbit
        symbolic_name:
            bnx2fc (QLogic BCM57810) v2.10.3 over em1.550
        tgtid_bind_type:
            wwpn (World Wide Port Name)
        uevent:
            DEVTYPE=scsi_host
        vport_create:
            <store method only>
        vport_delete:
            <store method only>
    host12:
        ----------
        ...
```

### [memory](memory.py)

  * __memory.usage__ - Return some informations on physical memory and swap
```bash
myserver:
    ----------
    MemAvailable:
         15 GB
    MemFree:
         11 GB
    MemTotal:
         15 GB
    SwapFree:
          2 GB
    SwapTotal:
          2 GB
```

### [pacemaker](pacemaker.py)

  * __cluster_local_node__
  * __cluster_local_node_status__
  * __cluster_name__
  * __cluster_nodes__
  * __cluster_nodes_status__
  * __cluster_resource_group_list__
  * __cluster_resources__
  * __cluster_service_status__
  * __cluster_stonith_configured__
  * __is_cluster_member__

### [rpmpkg](rpmpkg.py), [rpmlibpkg](rpmlibpkg.py)

  * __rpmpkg.buildtime__ - Return the build date and time
```bash
myserver:
    Fri Jan 27 23:18:03 2017
```

  * __rpmpkg.lastupdate__ - Return the date of the last rpm package update/installation
```bash
myserver:
    Fri Feb  3 12:38:13 2017
```

  * __rpmpkg.list_pkgs__ - List the packages currently installed in a dict
```bash
myserver:
    ----------
    GeoIP:
        1.5.0-11.el7.x86_64
    NetworkManager:
        1:1.4.0-13.el7_3.x86_64
    NetworkManager-config-server:
        1:1.4.0-13.el7_3.x86_64
    ...
 
    zip:
        3.0-11.el7.x86_64
    zlib:
        1.2.7-17.el7.x86_64

```

### [service_iana](service_iana.py)

  * __get_service_list__ - Return a dictionary of services recorded in /etc/services
```bash
myserver:
    ----------
    1/ddp:
        ----------
        name:
            rtmp
        port:
            1
        protocol:
            ddp
    1/tcp:
        ----------
        name:
            tcpmux
        port:
            1
        protocol:
            tcp
    ...
```

### [swap](swap.py)

  * __swap.usage__ - Return informations for swap filesystem
```bash
myserver:
    ----------
    /dev/mapper/rootvg-swaplv:
        ----------
        available:
            2.0GB
        device:
            /dev/dm-12
        priority:
            -1
        size:
            2.0GB
        used:
            0.0kB
```

[saltstackexec]: https://docs.saltstack.com/en/latest/ref/modules/
