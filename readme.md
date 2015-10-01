bkup
====

easily backup directories to remote and local devices

(`bkup` is written for Python 3)

## Setup
You should have your SSH keys on all remote machines you will be accessing.

For reference, you can do this like so:

```bash
$ ssh-copy-id <user>@<host>

# Example:
$ ssh-copy-id ftseng@pony.local
```


## Installation

    pip install bkup


## Configuration
Setup your backup configuration in `~/.bkup`.

It takes the format:

```yaml
task_name:
  dirs:
    - '~/some/local/dir'
    - '~/other/local/dir'
  targets:
    - 'me@somehost:/path/to/backup/to'
    - '/mnt/local/path/to/backup/to'
```

Note that this uses `rsync` underneath, which I have always found confusing, but as a target you specify the _parent_ directory you want to sync to.

For example, in the config above, the local directory `~/some/local/dir` is synced onto `somehost` at `/path/to/backup/to/dir`.

#### Safety option
The optional `never_delete` property is a setting which, if set to
`true`, will never destructively sync, even if the user specifies it.

This is useful, for instance, when you want to have an archiving task
which syncs local folders to the remote host but does not propagate
deletions. That way, you can delete files in the local folder
without them being deleted in the remote folder.


## Usage

To use, simply do:

    bkup <task name> [--delete]

The optional `--delete` flag will destructively sync (unless `never_delete` is set to `true` for the task).
