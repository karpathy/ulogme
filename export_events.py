import time
import datetime
import json
import os
import os.path
import sys
import glob


def loadEvents(fname):
  """
  Reads a file that consists of first column of unix timestamps
  followed by arbitrary string, one per line. Outputs as dictionary.
  Also keeps track of min and max time seen in global mint,maxt
  """
  events = []

  try:
    ws = open(fname, 'r').read().decode('utf-8').splitlines()
    events = []
    for w in ws:
      ix = w.find(' ') # find first space, that's where stamp ends
      stamp = int(w[:ix])
      str = w[ix+1:]
      events.append({'t':stamp, 's':str})
  except Exception, e:
    print '%s probably does not exist, setting empty events list.' % (fname, )
    print 'error was:'
    print e
    events = []
  return events

def mtime(f):
  """
  return time file was last modified, or 0 if it doesnt exist
  """
  if os.path.isfile(f):
    return int(os.path.getmtime(f))
  else:
    return 0

def updateEvents():
  """
  goes down the list of .txt log files and writes all .json
  files that can be used by the frontend
  """
  L = []
  L.extend(glob.glob("logs/keyfreq_*.txt"))
  L.extend(glob.glob("logs/window_*.txt"))
  L.extend(glob.glob("logs/notes_*.txt"))

  # extract all times. all log files of form {type}_{stamp}.txt
  ts = [int(x[x.find('_')+1:x.find('.txt')]) for x in L]
  ts = list(set(ts))
  ts.sort()

  mint = min(ts)
  maxt = max(ts)

  # march from beginning to end, group events for each day and write json
  ROOT = ''
  RENDER_ROOT = os.path.join(ROOT, 'render')
  os.system('mkdir -p ' + RENDER_ROOT) # make sure output directory exists
  t = mint
  out_list = []
  for t in ts:
    t0 = t
    t1 = t0 + 60*60*24 # 24 hrs later
    fout = 'events_%d.json' % (t0, )
    out_list.append({'t0':t0, 't1':t1, 'fname': fout})

    fwrite = os.path.join(RENDER_ROOT, fout)
    e1f = 'logs/window_%d.txt' % (t0, )
    e2f = 'logs/keyfreq_%d.txt' % (t0, )
    e3f = 'logs/notes_%d.txt' % (t0, )
    e4f = 'logs/blog_%d.txt' % (t0, )

    dowrite = False

    # output file already exists?
    # if the log files have not changed there is no need to regen
    if os.path.isfile(fwrite):
      tmod = mtime(fwrite)
      e1mod = mtime(e1f)
      e2mod = mtime(e2f)
      e3mod = mtime(e3f)
      e4mod = mtime(e4f)
      if e1mod > tmod or e2mod > tmod or e3mod > tmod or e4mod > tmod:
        dowrite = True # better update!
        print 'a log file has changed, so will update %s' % (fwrite, )
    else:
      # output file doesnt exist, so write.
      dowrite = True

    if dowrite:
      # okay lets do work
      e1 = loadEvents(e1f)
      e2 = loadEvents(e2f)
      e3 = loadEvents(e3f)
      for k in e2: k['s'] = int(k['s']) # int convert

      e4 = ''
      if os.path.isfile(e4f):
        e4 = open(e4f, 'r').read()

      eout = {'window_events': e1, 'keyfreq_events': e2, 'notes_events': e3, 'blog': e4}
      open(fwrite, 'w').write(json.dumps(eout))
      print 'wrote ' + fwrite

  fwrite = os.path.join(RENDER_ROOT, 'export_list.json')
  open(fwrite, 'w').write(json.dumps(out_list).encode('utf8'))
  print 'wrote ' + fwrite

# invoked as script
if __name__ == '__main__':
  updateEvents()
