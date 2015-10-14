import os
import re
import yaml
import click
import socket
import datetime
import subprocess
from itertools import combinations

rsync = ['rsync', '-avuhz', '--progress']


@click.command()
@click.argument('task')
@click.option('--delete', default=False, help='delete remote files not found locally. Ignored for sync tasks', is_flag=True)
def bkup(task, delete):
    with open(os.path.expanduser('~/.bkup'), 'r') as f:
        conf = yaml.load(f)

    if task not in conf:
        print('Task "{}" is not defined in your config.'.format(task))
        return
    task = conf[task]

    if task.get('sync', False):
        sync(task)
    else:
        push(task, delete)


def push(task, delete):
    """Push (broadcast) from one machine to many others"""
    if delete and not task.get('never_delete', False):
        rsync.append('--delete')

    for target in task['targets']:
        # simple check for remote hosts
        if '@' in target:
            # skip host if it is inaccessible
            host = re.search(r'@([^:]+)', target).group(1)
            if not ping_host(host):
                print('Host {0} is down, skipping...'.format(host))
                continue

        # simple check for local devices
        else:
            if not os.path.exists(target):
                print('Local target {} not found, skipping...'.format(target))
                continue

        # for each mapping for the host...
        for dir in task['dirs']:
            frm = os.path.expanduser(dir)

            nice_print('Backing up {0} to {1}...'.format(frm, target))
            run(rsync + [frm, target])

            # update the last updated file
            now = datetime.datetime.now()

            if '@' in target:
                host, dest = target.split(':')
                run(['ssh', host, 'echo "{0}" > {1}'.format(str(now), os.path.join(dest, '_lastupdated.txt'))])
            else:
                with open(os.path.join(target, '_lastupdated.txt'), 'w') as f:
                    f.write(str(now))


def sync(task):
    """Sync multiple machines together"""
    localhost = socket.gethostname()

    for a, b in combinations(task['targets'], 2):
        for frm, to in [(a,b),(b,a)]:
            print('\n\n{} --> {}\n'.format(frm, to))

            user_f, host_f, path_f = frm.replace('@', ':').split(':')
            user_t, host_t, path_t = to.replace('@', ':').split(':')

            # if the from and target hosts are the same,
            # the target user@host is redundant, remove it
            if host_f == host_t:
                to = path_t

            # if the from host is the localhost,
            # we can drop the ssh command
            if host_f == localhost:
                path_f = os.path.expanduser(path_f)
                cmd = rsync + [path_f, to]
            else:
                rsync_cmd = '{} {} {}'.format(' '.join(rsync),
                                              path_f,
                                              to)
                cmd = ['ssh', '{}@{}'.format(user_f, host_f), rsync_cmd]
            run(cmd)



def ping_host(host):
    """Check to see if a host is available"""
    try:
        subprocess.check_call(['ping', '-c', '1', host],
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def run(cmd):
    """Run a command and print its output realtime"""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE)

    for line in iter(process.stdout.readline, b''):
        print(line.decode('utf-8').replace('\n', ''))


def nice_print(msg):
    """Make it look nice :)"""
    print('\n\033[93m===========================================\033[0m')
    print('\033[94m{msg}\033[0m'.format(msg=msg))
    print('\033[93m===========================================\033[0m\n')
