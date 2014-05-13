
# ulogme

Wondering where your day went? How productive were you today? How much code have you written?

Keep track of your productivity throughout the day. First commit are just a few scripts that gather data. Future commits will include some of my currently messy code for actually analyzing the logs and creating report webpages.

- `keyfreq.sh` logs the frequency of keystrokes in 9 second windows. This is a proxy for how much stuff (especially code) you write.
- `logactivewin.sh` logs the name of the current active window every 2 seconds.
- `logdesktop.sh` logs screenshot every 1 minute to a directory.
- `note.sh` simply logs a note. I use it for things such as "coffee medium", or "slept 6", etc... I can later correlate these notes to how productive I was, or any other notes or events.

These only work on Ubuntu. I usually have several terminal windows with some of these running and separate (not yet published) analysis files that report on statistics for every day.

BSD 2 clause license
