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
        secgroups:
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
        class:
            system
        device:
            /dev/mapper/rootvg-rootlv
        scope:
            Unknown
        size:
            1.9GB
        type:
            ext4
        used:
            40.3MB
    /boot:
        ----------
        autofs:
            false
        automount:
            true
        available:
            184.2MB
        class:
            system
        device:
            /dev/mapper/mpatha1
        scope:
            Unknown
        size:
            379.4MB
        type:
            ext4
        used:
            171.1MB
    /sharednfs:
        ----------
        autofs:
            false
        automount:
            true
        available:
            477.1GB
        class:
            other
        device:
            nas.domain.local:/PARTNFS/sharedfolder
        scope:
            lan
        size:
            2.0TB
        type:
            nfs
        used:
            1.5TB
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
