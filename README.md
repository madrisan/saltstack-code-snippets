![](images/saltstack_horizontal_dark.png?raw=true)

# SaltStack code snippets for Linux

A set of code snippets that can be used to build SaltStack [execution modules][saltstackexec].

### cpuinfo
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

### fsinfo
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

### rpmpck
  * __rpmpck.lastupdate__ - Return the date of the last rpm package update/installation
```bash
myserver:
    Fri Feb  3 12:38:13 2017
```

  * __rpmpck.buildtime__ - Return the build date and time
```bash
myserver:
    Fri Jan 27 23:18:03 2017
```

[saltstackexec]: https://docs.saltstack.com/en/latest/ref/modules/
