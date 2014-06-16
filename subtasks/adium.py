import os
import shutil

def run(target):
    path = os.path.expanduser(target)
    adium_dir = os.path.expanduser('~/Library/Application Support/Adium 2.0')

    if os.path.exists(path):
        shutil.rmtree(path)

    shutil.copytree(adium_dir, path)
