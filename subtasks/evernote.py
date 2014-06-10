import subprocess

def run():
    process = subprocess.Popen(
        ['osascript', 'scripts/backup_evernote.scpt'],
        stdout=subprocess.PIPE)
    process.wait()
