backitup
========

A super cool back up script.

It's tailored to my backup setup, which involves one remote machine with a few attached external HDDs.

## Setup
You should have your SSH keys on all remote machines you will be
accessing.

For reference, you can do this like so:

```bash
$ ssh-copy-id <user>@<host>

# Example:
$ ssh-copy-id ftseng@pony.local
```

## Configuration
Setup your backup configuration in `config.json`.

It takes the format:

```json
{
    "<task name>": {
        "<remote hostname>": {
            "user": "<remote user>",
            "mappings": {
                "<local path>": "<remote path>"
            },
            "externals": {
                "<remote path>": ["<ext hdd path>"]
            },
            "never_delete": false
        },
        "subtasks": ["<subtask module name>"]
    }
}
```

#### Mappings
The `mappings` property maps the folders on the local machine
(i.e. the machine executing this script) to the backup folders on the remote machine.

#### External HDDs
The `externals` property maps folders on the *remote* machine to
external hard drives (specified as paths) attached to the *remote* machine. This assumes OSX
(i.e. it looks for the specified paths in `/Volumes/`).

The external hard drives *do not* have to be present; the script
will check if they are there before attempting to sync to them.

#### Safety option
The optional `never_delete` property is a setting which, if set to
`true`, will never destructively sync, even if the user specifies it.

This is useful, for instance, when you want to have an archiving task
which syncs local folders to the remote host but does not propagate
deletions. That way, you can delete files in the local folder
without them being deleted in the remote folder.

#### Subtasks
You can add modules to the `subtasks/` directory which can then be
specified as subtasks to be run at the start of the task. Refer to them
by the name of the module.

The only requirement is that the subtask module has a `run` method which
does whatever you want it to do.


## Usage
To use, simply do:

```bash
$ python backitup.py <task name> [--delete]

# Example
$ python backitup.py backup --delete
```

The optional `--delete` flag will destructively sync (unless of course
`never_delete` is set to `true` for the task).

## Configuration Example

```json
{
    "backup": {
        "pony.local": {
            "user": "ftseng",
            "mappings": {
                "~/Desktop/special_sauce": "~/Desktop/backups"
            },
            "externals": {
                "~/Desktop/backups": ["superdrive/foobar"]
            }
        },
        "subtasks": ["evernote"]
    }
}
```

This will sync the local `~/Desktop/special_sauce` folder to the
`~/Desktop/backups` folder on the remote host `pony.local`. When that
syncing is complete, it will sync the remote folder `~/Desktop/backups`
to the remote external hard drive at `/Volumes/superdrive` to its
`foobar` folder.
