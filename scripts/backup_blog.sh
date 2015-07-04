# for nearlyfreespeech.net (NFS), you can add a public key by going to the Profile tab when you're logged in.
# just paste in the output of `cat ~/.ssh/id_rsa.pub`.

USER=theneonzoo_spaceandtimes
HOST=ssh.phx.nearlyfreespeech.net
BACKUP_DIR=~/STUFF/backups
mkdir -p $BACKUP_DIR/spaceandtimes/uploads

PASS=$1

# Back up the database.
# You do need to enter your mysql password here. For NFS, it should just be your user password, unless you've changed it.
ssh $USER@$HOST 'mysqldump --compact --quick --host=publicscience.db --user=theneonzoo --password='"'"$PASS"'"' spaceandtimes > spaceandtimes.sql; tar -pczf spaceandtimes.tgz spaceandtimes.sql; rm spaceandtimes.sql'
scp $USER@$HOST:/home/public/spaceandtimes.tgz /tmp/
ssh $USER@$HOST 'rm spaceandtimes.tgz'
tar -xzvf /tmp/spaceandtimes.tgz
mv spaceandtimes.sql $BACKUP_DIR/spaceandtimes/

# Back up uploads.
rsync -rva $USER@$HOST:/home/public/uploads/ $BACKUP_DIR/spaceandtimes/uploads
