backitup
========

A collection of my back up scripts.
They all really only use `rsync`. When I say "backs up from A to B", I
basically mean, "keep B in sync with A".

## Setup

### Main (local) machine
My home directory (`~`) structure looks something like this:
```
├── Desktop
│   ├── STUFF
│   ├── graphics
│   ├── informations
│   ├── projects
│   └── work
├── Downloads
    └── mytv
```

(there are of course other directories but these are the important ones)


### Remote machine
There is a remote machine (in these scripts it is named `pony.local`)
where backups go to.

The remote machine has a home directory structure like:
```
├── Desktop
│   ├── backup
│   ├── repos
│   ├── archives
│   └── tv
```


### External HDDs
There is also a collection of hard drives that also serve as backup
locations. There is a primary one, known in these scripts as `outerspace`.


## The scripts

There are a few scripts, each with a different functionality:

`backitup`

Backs up the local machine's `Desktop` directories to the
remote machine's `repos` directory. Then it calls the `backitup.pony` on
the remote machine (see below).

Takes an optional `delete` argument which will delete files no longer on
the local machine (i.e. a destructive sync).

---

`backitup.pony`

Backs up the remote machine's `repos`, `archives`, and `tv` to the `outerspace` ext
HDD. This does NOT include its `backup` directory.

Takes an optional `delete` argument which will delete files no longer on
the local machine (i.e. a destructive sync).

```bash
$ sh backitup [delete]
```

---

`backitup.mini`

Backs up from the local (or remote, depends where it
is run) machine to an auto-detected external HDD.

The valid names of volumes are specified in the script.

Takes an optional `delete` argument which will delete files no longer on
the local machine (i.e. a destructive sync).

```bash
$ sh backitup.mini [delete]
```

---

`fullbackitup`

The same as `backitup`, except it additionally backs
up the local machine's `Downloads` as well as it's SSH keys. These
additional files are sent to the remote machines `backup` directory.

Takes an optional `delete` argument which will delete files no longer on
the local machine (i.e. a destructive sync).

```bash
$ sh fullbackitup [delete]
```
