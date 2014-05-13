#!/bin/bash

# Logs the number of keys pressed during every 9 second interval
# into keyfreq/keyfreq.txt. Two columns are saved on every line:
# 1st column: unix time
# 2nd column: number of keystrokes during last 9 seconds

mkdir -p keyfreq

while true
do
  showkey > keyfreq/raw.txt &
  PID=$!
  
  # work in windows of 9 seconds 
  sleep 9
  kill $PID
  
  # count number of key release events
  num=`cat keyfreq/raw.txt | grep release | wc -l`
  
  # append unix time stamp and the number into file
  echo "$(date +%s) $num"  >> keyfreq/keyfreq.txt
  echo "$(date) $num release events detected"
  
done

