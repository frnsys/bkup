backitup
========

A collection of my back up (rsync) scripts.

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

The `archives` and `tv` folders have stuff manually added to them.
They are then non-destructively backed up to external HDDs (that is,
the deletion of files are not synced).

### External HDDs
There is also a collection of hard drives that also serve as backup
locations. There is a primary one, known in these scripts as `outerspace`.

---

## The scripts
There are a few scripts, each with a different functionality:

`backitup`
`local => remote => externals`

Takes an optional `delete` argument which will delete files no longer on
the local machine (i.e. a destructive sync).

```bash
$ sh backitup [--delete]
```
---

`backitup.mini`
`local => externals`

Backs up to auto-detected specified external HDDs.
The valid names of volumes are specified in the script.

Takes an optional `delete` argument which will delete files no longer on
the local machine (i.e. a destructive sync).

```bash
$ sh backitup.mini [--delete]
```

---

`backitup.full`

The same as `backitup`, except it additionally backs
up the local machine's `Downloads` as well as it's SSH keys. These
additional files are sent to the remote machines `backup` directory.

Takes an optional `delete` argument which will delete files no longer on
the local machine (i.e. a destructive sync).

```bash
$ sh backitup.full [--delete]
```
