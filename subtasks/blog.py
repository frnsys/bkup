import subprocess
import values

def run():
    process = subprocess.Popen(
        ['bash', 'scripts/backup_blog.sh', values.NFS_MYSQL_PW],
        stdout=subprocess.PIPE)
    process.wait()
