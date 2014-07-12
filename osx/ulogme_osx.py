import sys, os, time
from threading import Timer
from optparse import OptionParser, make_option

from Foundation import NSObject, NSLog
from AppKit import NSApplication, NSApp, NSWorkspace
from Cocoa import *
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
from PyObjCTools import AppHelper

def current_time():
  """
  Get a current UNIX timestamp.
  """
  return int(time.time())


class EventSniffer:

  def createAppDelegate(self):
    _self = self
    class AppDelegate(NSObject):
      def applicationDidFinishLaunching_(self, notification):
        mask = NSKeyDownMask | NSLeftMouseDownMask | NSRightMouseDownMask | NSScrollWheelMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, _self.handler)
        NSEvent.addLocalMonitorForEventsMatchingMask_handler_(mask, _self.handler)
    return AppDelegate
  
  def __init__(self, options):
    self.current_app = None
    self.current_window = None
    self.options = options
    self.num_keystrokes = 0
    
  def run(self):
    NSApplication.sharedApplication()
    delegate = self.createAppDelegate().alloc().init()
    NSApp().setDelegate_(delegate)
    self.workspace = NSWorkspace.sharedWorkspace()
    
    self.write_keystrokes()
    AppHelper.runEventLoop()

  def handler(self, event):
    self.maybe_write_current_app()
    if event.type() == NSKeyDown:
      self.num_keystrokes += 1
        
  def get_current_app(self):
    running_apps = self.workspace.runningApplications()
    for app in running_apps:
      if app.isActive():
        return app.localizedName()

  def get_current_window_name(self):
    options = kCGWindowListOptionOnScreenOnly
    window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in window_list:
      if window['kCGWindowOwnerName'] == self.get_current_app():
        window_name = window['kCGWindowName']
        return window_name

  def maybe_write_current_app(self):
    current_app = self.get_current_app()
    if current_app != self.current_app:
      # Write the timestamp and current app to file
      self.current_app = current_app
      with open(self.options.active_window_file, 'a') as f:
       f.write('%d %s\n' % (current_time(), self.current_app))

  def write_keystrokes(self):
    """
    Write the number of keystrokes to output file, and schedule
    another call of this method.
    """
    with open(self.options.keystroke_file, 'a') as f:
      f.write('%d %d\n' % (current_time(), self.num_keystrokes))
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

  with open(options.pid_file, 'w') as f:
    f.write(str(os.getpid()))

  app = EventSniffer(options)
  app.run()

