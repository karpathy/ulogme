#!/bin/bash

# every 2 seconds looks at active window and if it has changed
# the change gets recorded in activewin/log.txt together with 
# the unix time of the change

waittime="2" # number of seconds between executions of loop
logfile="logs/activewin.txt" # output file
mkdir -p logs
#------------------------------

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

	# log new window switch, unless screensaver is running
	if [[ "$lasttitle" != "$curtitle" ]]; then 
		# number of seconds elapsed since Jan 1, 1970 0:00 UTC
		T="$(date +%s)"
		echo "$(date) $curtitle"
		echo "$T $curtitle" >> "$logfile"
	fi

	# swap
	lasttitle="$curtitle"
	sleep "$waittime"
done




