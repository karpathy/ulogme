import time
import datetime
import json
import os
import os.path

ROOT = ''
RENDER_ROOT = os.path.join(ROOT, 'render')

mint = -1
maxt = -1

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
    print e
    events = []
  return events

# load all window events
active_window_file = ROOT + 'logs/activewin.txt'
print 'loading windows events...'
wevents = loadEvents(active_window_file)

# load all keypress events
keyfreq_file = ROOT + 'logs/keyfreq.txt'
print 'loading key frequencies...'
kevents = loadEvents(keyfreq_file)
for k in kevents: # convert the key frequency to just be an int, not string
  k['s'] = int(k['s'])

print 'loading notes...'
notes_file = ROOT + 'logs/notes.txt'
nevents = loadEvents(notes_file)

# coming soon
#music_file = ROOT + 'music/music.txt'
#print 'loading music...'
#mevents = loadEvents(music_file)

os.system('mkdir -p ' + RENDER_ROOT) # make sure output directory exists

# rewind time to 7am on earliest data collection day
dfirst = datetime.datetime.fromtimestamp(mint)
dfirst = datetime.datetime(dfirst.year, dfirst.month, dfirst.day, 7) # set hour to 7am
curtime = int(dfirst.strftime("%s"))
out_list = []
while curtime < maxt:
  t0 = curtime
  t1 = curtime + 60*60*24 # one day later
  e1 = [x for x in wevents if x['t'] >= t0 and x['t'] < t1]
  e2 = [x for x in kevents if x['t'] >= t0 and x['t'] < t1]
  e3 = [x for x in nevents if x['t'] >= t0 and x['t'] < t1]
  eout = {'window_events': e1, 'keyfreq_events': e2, 'notes_events': e3}
  fout = 'events_%d.json' % (t0, )
  out_list.append({'t0':t0, 't1':t1, 'fname': fout})
  fwrite = os.path.join(RENDER_ROOT, fout)
  open(fwrite, 'w').write(json.dumps(eout))
  print 'wrote ' + fwrite
  curtime += 60*60*24

fwrite = os.path.join(RENDER_ROOT, 'export_list.json')
open(fwrite, 'w').write(json.dumps(out_list))
print 'wrote ' + fwrite
