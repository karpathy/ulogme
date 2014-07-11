import sys, os, calendar, time
from optparse import OptionParser, make_option
from threading import Timer

from Foundation import NSObject, NSLog
from AppKit import NSApplication, NSApp, NSWorkspace
from Cocoa import *
from PyObjCTools import AppHelper

def current_time():
  """
  Get a current UNIX timestamp. This is surprisingly awkward in Python.
  """
  return calendar.timegm(time.gmtime())


class EventSniffer:

  def createAppDelegate(self):
    _self = self
    class AppDelegate(NSObject):
      def applicationDidFinishLaunching_(self, notification):
        mask = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, _self.handler)
        NSEvent.addLocalMonitorForEventsMatchingMask_handler_(mask, _self.handler)
    return AppDelegate
  
  def __init__(self, options):
    self.current_app = None
    self.options = options
    self.num_keystrokes = 0
    
  def run(self):
    NSApplication.sharedApplication()
    delegate = self.createAppDelegate().alloc().init()
    NSApp().setDelegate_(delegate)
    self.workspace = NSWorkspace.sharedWorkspace()
    
    Timer(self.options.active_window_time, self.write_current_app).start()
    Timer(self.options.keystroke_time, self.write_keystrokes).start()

    AppHelper.runEventLoop()

  def handler(self, event):
    if event.type() == NSKeyDown:
      self.num_keystrokes += 1
        
  def get_current_app(self):
    running_apps = self.workspace.runningApplications()
    for app in running_apps:
      if app.isActive():
        return app.localizedName()

  def write_current_app(self):
    current_app = self.get_current_app()
    if current_app != self.current_app:
      # Write the timestamp and current app to file
      self.current_app = current_app
      with open(self.options.active_window_file, 'a') as f:
       f.write('%d %s\n' % (current_time(), self.current_app))

    # Schedule this check to happen again
    Timer(self.options.active_window_time, self.write_current_app).start()

  def write_keystrokes(self):
    with open(self.options.keystroke_file, 'a') as f:
      f.write('%d %s\n' % (current_time(), self.num_keystrokes))
    self.num_keystrokes = 0
    Timer(self.options.keystroke_time, self.write_keystrokes).start()


if __name__ == '__main__':
  option_list = [
      make_option('--pid_file',
                  action='store',
                  dest='pid_file',
                  default=None,
                  help='Required.'),
      make_option('--keystroke_file',
                  action='store',
                  dest='keystroke_file',
                  default=None,
                  help='Required.'),
      make_option('--active_window_file',
                  action='store',
                  dest='active_window_file',
                  default=None,
                  help='Required.'),
      make_option('--keystroke_time',
                  action='store',
                  dest='keystroke_time',
                  default=9,
                  help='Time (in seconds) between recording keystrokes'),
      make_option('--active_window_time',
                  action='store',
                  dest='active_window_time',
                  default=2,
                  help='Time (in seconds) between polling active window'),
  ]

  parser = OptionParser(option_list=option_list)
  (options, args) = parser.parse_args()
  for option in option_list:
    if getattr(options, option.dest) is None:
      parser.print_help()
      sys.exit(1)

  with open('.python_pid', 'w') as f:
    f.write(str(os.getpid()))

  app = EventSniffer(options)
  app.run()

