#!/bin/bash

# This script should automatically be run by the remote version of backitup
# after it has finished backing up the remote computer to this computer.

# This script will back up these specified local directories to attached external HDDs.
# To add other harddrives, just add other rsync lines pointing to the appropriate
# HDD, such as /Volumes/myexthdd

if [[ $1 == "delete" ]]
then
	echo "Are you sure you want to rsync with the delete flag? y/n"
	read a
	if [[ $a == "Y" || $a == "y" ]]; then
		rsync -avu --progress --delete ~/Desktop/repos /Volumes/outerspace
		rsync -avu --progress --delete ~/Desktop/tv /Volumes/outerspace
		rsync -avu --progress --delete ~/Desktop/archives /Volumes/outerspace
	else
	  echo "Not doing it"
	fi
else
	rsync -avu --progress ~/Desktop/repos /Volumes/outerspace
	rsync -avu --progress ~/Desktop/tv /Volumes/outerspace
	rsync -avu --progress ~/Desktop/archives /Volumes/outerspace
fi
