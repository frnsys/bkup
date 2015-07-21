import subprocess
import argparse
import datetime
import pipes
import json
import os

import subtasks

def main():
    args = parse_args()

    task = load_task(args.task)
    if not task:
        return

    #rsync = ['rsync', '-avuhz', '--progress', '--checksum']
    rsync = ['rsync', '-avuhz', '--progress']
    if args.delete and not task.get('never_delete', False):
        rsync.append('--delete')

    # Run subtasks...
    for subtask, params in task.get('subtasks', {}).items():
        print('Running subtask `{0}`...'.format(subtask))
        subtasks.namespace[subtask].run(*params)
    task.pop('subtasks', None)

    # For each host in the task...
    for host, settings in task.items():

        if host != 'localhost':
            # Skip host if it is inaccessible.
            if not ping_host(host):
                print('Host {0} is down, skipping...'.format(host))
                continue

            user = settings['user']
            remote = '{0}@{1}'.format(user, host)
        else:
            remote = ''


        # For each mapping for the host...
        for src, dests in settings.get('mappings', {}).items():
            if not isinstance(dests, list):
                dests = [dests]

            for dest in dests:
                frm = os.path.expanduser(src)

                if remote:
                    to = '{0}:{1}'.format(remote, dest)
                else:
                    # Skip path if it does not exist
                    if not os.path.exists(dest):
                        print('\nLocal path {0} not found, skipping...'.format(dest))
                        continue
                    to = dest

                nice_print('Backing up {0} to {1}...'.format(frm, to))
                run(rsync + [frm, to])

                # Update the last updated file.
                now = datetime.datetime.now()

                if remote:
                    run(['ssh', remote, 'echo "{0}" > {1}'.format(str(now), os.path.join(dest, '_lastupdated.txt'))])
                else:
                    with open(os.path.join(dest, '_lastupdated.txt'), 'w') as f:
                        f.write(str(now))

        # Backup to external HDDs attached to the remote machine...
        if remote:
            for remote_src, ext_hdds in settings.get('externals', {}).items():
                for ext_hdd_path in ext_hdds:
                    if remote_path_exists(remote, ext_hdd_path):
                        nice_print('Drive {0} was found, backing up to it...'.format(ext_hdd_path))

                        # Build the remote rsync command.
                        remote_rsync = '{rsync} {src} {dest}'.format(
                                rsync=' '.join(rsync),
                                src=remote_src,
                                dest=ext_hdd_path
                        )

                        run(['ssh', remote, remote_rsync])

def parse_args():
    """
    Handle the arguments
    for this script.
    """
    parser = argparse.ArgumentParser(
                description='manage and update backups.'
             )
    parser.add_argument('task', type=str, help='the particular backup task to run.')
    parser.add_argument('--delete', action='store_true', help='whether or not to sync deleted files.')
    return parser.parse_args()

def ping_host(host):
    """
    Check to see if a host
    is available.
    """
    try:
        subprocess.check_call(['ping', '-c', '1', host],
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def load_task(task):
    """
    Load a task config
    by name.
    """
    config = json.load(open('config.json'))
    task_config = config.get(task)

    # Check if task exists.
    if not task_config:
        nice_print('Task by the name "{0}" could not be found.'.format(task))
        print('Available tasks are:')
        print(' '.join([k for k in config.keys()]))
        return False
    return task_config

def run(cmd):
    """
    Run a command
    and print its output realtime.
    """
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE)

    for line in iter(process.stdout.readline, ''):
        print(line.replace('\n', ''))

def nice_print(msg):
    """
    Make it look nice :)
    """
    print('\n\033[93m===========================================\033[0m')
    print('\033[94m{msg}\033[0m'.format(msg=msg))
    print('\033[93m===========================================\033[0m\n')

def remote_path_exists(remote, path):
    """
    Check if a path exists
    on a remote machine.
    """
    return subprocess.call(['ssh', remote, 'test -e ' + pipes.quote(path)]) == 0

if __name__ == '__main__':
    main()
