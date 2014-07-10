"""
This script exports Evernote notes
to ~/Desktop/STUFF/backups/.
"""

import subprocess

def run():
    process = subprocess.Popen(
        ['osascript', 'scripts/backup_evernote.scpt'],
        stdout=subprocess.PIPE)
    process.wait()
