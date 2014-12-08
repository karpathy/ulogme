#!/bin/bash

LANG=en_US.utf8

# logs the active window titles over time. Logs are written 
# in logs/windowX.txt, where X is unix timestamp of 7am of the
# recording day. The logs are written if a window change event occurs
# (with 2 second frequency check time), or every 10 minutes if 
# no changes occur.

waittime="2" # number of seconds between executions of loop
maxtime="600" # if last write happened more than this many seconds ago, write even if no window title changed
#------------------------------

mkdir -p logs
last_write="0"
lasttitle=""
while true
do

	islocked=true; if [[ $(gnome-screensaver-command -q) =~ .*inactive.* ]]; then islocked=false; fi
	if [ $islocked = true ]; then
		curtitle="__LOCKEDSCREEN"
	else 
		id=$(xdotool getactivewindow)
		curtitle=$(wmctrl -lpG | while read -a a; do w=${a[0]}; if (($((16#${w:2}))==id)) ; then echo "${a[@]:8}"; break; fi; done)
	fi

	perform_write=false

	# if window title changed, perform write
	if [[ "$lasttitle" != "$curtitle" ]]; then
		perform_write=true
	fi

	T="$(date +%s)"
	
	# if more than some time has elapsed, do a write anyway
	#elapsed_seconds=$(expr $T - $last_write)
	#if [ $elapsed_seconds -ge $maxtime ]; then
	#	perform_write=true
	#fi

	# log window switch if appropriate
	if [ "$perform_write" = true ]; then 
		# number of seconds elapsed since Jan 1, 1970 0:00 UTC
		logfile="logs/window_$(python rewind7am.py).txt"
		echo "$T $curtitle" >> $logfile
		echo "logged window title: $(date) $curtitle into $logfile"
		last_write=$T
	fi

	lasttitle="$curtitle" # swap
	sleep "$waittime" # sleep
done




