#!/bin/bash

# periodically takes screenshot and saves them to desktopscr/
# the filename contains unix time

# wait time in seconds
waittime="60"
# directory to save screenshots to
saveprefix="desktopscr/scr"
mkdir -p desktopscr

#------------------------------

while true
do
	islocked=true; if [[ $(gnome-screensaver-command -q) =~ .*inactive.* ]]; then islocked=false; fi

	if ! $islocked
	then
		# take screenshot into file
		T="$(date +%s)"
		fname="$saveprefix_$T.jpg"
		# q is quality. Higher is higher quality
		scrot -q 50 "$fname"
	else
		echo "screen is locked, waiting..."
	fi

	sleep $waittime
done


