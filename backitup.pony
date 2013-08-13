#!/bin/bash

# This script should automatically be run by the remote version of backitup
# after it has finished backing up the remote computer to this computer.


delete=""
if [[ $1 == "--delete" ]]
then
	echo "Are you sure you want to rsync with the delete flag? y/n"
	read a
	if [[ $a == "Y" || $a == "y" ]]; then
        delete="--delete"
	else
	  echo "Not doing it"
	fi
fi

rsync -avu --progress $delete ~/Desktop/repos /Volumes/outerspace
rsync -avu --progress $delete ~/Desktop/tv /Volumes/outerspace
rsync -avu --progress $delete ~/Desktop/archives /Volumes/outerspace

bash backitup.mini $delete
