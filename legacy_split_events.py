# convert old type events to new type events, in case you used legacy ulogme code
# where all events were written to one file based on type. In new version these are
# split also by date.

import time
import datetime
import json
import os
import os.path
import sys

mint = -1
maxt = -1

ROOT = ''
RENDER_ROOT = os.path.join(ROOT, 'render')


def loadEvents(fname):
  """
  Reads a file that consists of first column of unix timestamps
  followed by arbitrary string, one per line. Outputs as dictionary.
  Also keeps track of min and max time seen in global mint,maxt
  """
  global mint, maxt # not proud of this, okay?
  events = []

  try:
    ws = open(fname, 'r').read().splitlines()
    events = []
    for w in ws:
      ix = w.find(' ') # find first space, that's where stamp ends
      stamp = int(w[:ix])
      str = w[ix+1:]
      events.append({'t':stamp, 's':str})
      if stamp < mint or mint==-1: mint = stamp
      if stamp > maxt or maxt==-1: maxt = stamp
  except Exception, e:
    print 'could not load %s. Setting empty events list.' % (fname, )
    print '(this is probably OKAY by the way, just letting you know)'
    print e
    events = []
  return events

# load all window events
active_window_file = os.path.join(ROOT, 'logs/activewin.txt')
print 'loading windows events...'
wevents = loadEvents(active_window_file)

# load all keypress events
keyfreq_file = os.path.join(ROOT, 'logs/keyfreq.txt')
print 'loading key frequencies...'
kevents = loadEvents(keyfreq_file)
for k in kevents: # convert the key frequency to just be an int, not string
  k['s'] = int(k['s'])

print 'loading notes...'
notes_file = os.path.join(ROOT, 'logs/notes.txt')
nevents = loadEvents(notes_file)

# rewind time to 7am on earliest data collection day
dfirst = datetime.datetime.fromtimestamp(mint)
dfirst = datetime.datetime(dfirst.year, dfirst.month, dfirst.day, 7) # set hour to 7am
curtime = int(dfirst.strftime("%s"))
out_list = []
while curtime < maxt:
  t0 = curtime
  t1 = curtime + 60*60*24 # one day later
  # this will break if there are leap seconds... sigh :D

  # filter events
  e1 = [x for x in wevents if x['t'] >= t0 and x['t'] < t1]
  e2 = [x for x in kevents if x['t'] >= t0 and x['t'] < t1]
  e3 = [x for x in nevents if x['t'] >= t0 and x['t'] < t1]

  # sort by time just in case
  e1.sort(key = lambda x: x['t'])
  e2.sort(key = lambda x: x['t'])
  e3.sort(key = lambda x: x['t'])

  # write out log files split up
  if e3:
    fout = 'logs/notes_%d.txt' % (t0, )
    f = open(fout, 'w')
    f.write(''.join( ['%d %s\n' % (x['t'], x['s']) for x in e3] ))
    f.close()
    print 'wrote ' + fout

  if e2:
    fout = 'logs/keyfreq_%d.txt' % (t0, )
    f = open(fout, 'w')
    f.write(''.join( ['%d %s\n' % (x['t'], x['s']) for x in e2] ))
    f.close()
    print 'wrote ' + fout

  if e1:
    fout = 'logs/window_%d.txt' % (t0, )
    f = open(fout, 'w')
    f.write(''.join( ['%d %s\n' % (x['t'], x['s']) for x in e1] ))
    f.close()
    print 'wrote ' + fout

  curtime += 60*60*24
