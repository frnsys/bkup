bkup
====

easily backup directories to remote and local devices and sync data between devices.

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

Note that this uses `rsync` underneath, so just be aware of how it handles source paths with and without trailing slashes differently ([here is a quick explanation](http://serverfault.com/questions/529287/rsync-creates-a-directory-with-the-same-name-inside-of-destination-directory)).

For example, in the config above, the source directory `~/some/local/dir` is synced onto `somehost` at `/path/to/backup/to/dir`.
If the source directory had ended with a trailing slash, i.e. `~/some/local/dir/` is synced onto `somehost` at `/path/to/backup/to`.

### Modes
`bkup` has two modes:

- __push__: backup files from one machine to many machines (default)
- __sync__: syncs files of multiple machines to each other

To use the __sync__ mode, just add `sync: true` to a task's configuration.

The __sync__ mode should not have any `dirs` specified because it treats all directories as remote.

### Deleting files and the safety option
For __push__ mode, the optional `never_delete` property is a setting which,
if set to `true`, will never destructively sync, even if the user specifies it
with the `--delete` flag.

This is useful, for instance, when you want to have an archiving task
which syncs local folders to the remote host but does not propagate
deletions. That way, you can delete files in the local folder
without them being deleted in the remote folder.

__Sync__ mode never deletes anything. So if you rename a file, you will need to
manually delete the old file from other devices. If you delete a file, you will need to
manually delete it from other devices.


## Usage

To use, simply do:

    bkup <task name> [--delete]

The optional `--delete` flag will destructively sync (unless `never_delete` is set to `true` for the task or it is a __sync__ task).
