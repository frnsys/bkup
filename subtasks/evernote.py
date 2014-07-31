"""
This script exports Evernote notes
to ~/Desktop/STUFF/backups/.

NOTE: For this to work, you cannot use
the Evernote installed from the App Store.
Use the one downloaded from their site.
"""

import subprocess

def run():
    process = subprocess.Popen(
        ['osascript', 'scripts/backup_evernote.scpt'],
        stdout=subprocess.PIPE)
    process.wait()
