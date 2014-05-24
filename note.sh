#!/bin/bash

# allows the user to simply record a note, saves it together with unix time in notes/

mkdir -p notes

read -p "Enter note: " n

if [ -z $1 ] 
then 
  # $1 was provided, use it
  echo "saving new note \"$n\" for current time ($(date))"
  T="$(date +%s)"
  echo "$T $n" >> notes/notes.txt
 
else
  # no $1 provided, use current time
  echo "saving new note \"$n\" for given time ($1)"
  echo "$1 $n" >> notes/notes.txt
fi

