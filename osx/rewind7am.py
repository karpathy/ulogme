import sys
import datetime
import time

def rewindTime(t):
  """
  very simply utility function that takes unix time (as int)
  and returns unix time at 7am of the day that the corresponding ulogme
  event belongs to. ulogme day breaks occur at 7am, so e.g. 3am late
  night session will count towards previous day activity
  """
  d = datetime.datetime.fromtimestamp(t)
  if d.hour >= 7:
    # it's between 7am-11:59pm
    d = datetime.datetime(d.year, d.month, d.day, 7) # rewind time to 7am
  else:
    # it's between 12am-7am, so this event still belongs to previous day
    d = datetime.datetime(d.year, d.month, d.day, 7) # rewind time to 7am
    d -= datetime.timedelta(days=1) # subtract a day

  curtime = int(d.strftime("%s"))
  return curtime

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    # use right now
    print rewindTime(int(time.time()))
  else:
    print rewindTime(int(sys.argv[1]))