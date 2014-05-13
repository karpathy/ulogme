#!/bin/bash

# allows the user to simply record a note, saves it together with unix time in notes/

mkdir -p notes

read -p "Enter note: " n

echo "$(date) new note saved:"
echo $n

T="$(date +%s)"
echo "$T $n" >> notes/notes.txt


