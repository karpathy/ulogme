import time
import datetime
import json
import os
import os.path

ROOT = ''
RENDER_ROOT = os.path.join(ROOT, 'render')

mint = -1
maxt = -1

# these two look very similar but keeping them flat and separate for future

# load all window events
active_window_file = ROOT + 'activewin/log.txt'
ws = open(active_window_file, 'r').read().splitlines()
wevents = []
for w in ws:
  ix = w.find(' ') # find first space, that's where stamp ends
  stamp = int(w[:ix])
  title = w[ix+1:]
  wevents.append({'t':stamp, 's':title})
  if stamp < mint or mint==-1: mint = stamp
  if stamp > maxt or maxt==-1: maxt = stamp
print 'loaded active windows'

# load all keypress events
keyfreq_file = ROOT + 'keyfreq/keyfreq.txt'
ws = open(keyfreq_file, 'r').read().splitlines()
kevents = []
for w in ws:
  ix = w.find(' ') # find first space, that's where stamp ends
  stamp = int(w[:ix])
  freq = int(w[ix+1:]) # number of keystrokes
  kevents.append({'t':stamp, 'f':freq})
  if stamp < mint or mint==-1: mint = stamp
  if stamp > maxt or maxt==-1: maxt = stamp
print 'loaded key frequencies'

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
  eout = {'window_events': e1, 'keyfreq_events': e2}
  fout = 'events_%d.json' % (t0, )
  out_list.append({'t0':t0, 't1':t1, 'fname': fout})
  fwrite = os.path.join(RENDER_ROOT, fout)
  open(fwrite, 'w').write(json.dumps(eout))
  print 'wrote ' + fwrite
  curtime += 60*60*24

fwrite = os.path.join(RENDER_ROOT, 'export_list.json')
open(fwrite, 'w').write(json.dumps(out_list))
print 'wrote ' + fwrite
