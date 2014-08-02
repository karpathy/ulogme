import sys, os, time, signal
from threading import Timer, Thread
from optparse import OptionParser, make_option

from Foundation import NSObject, NSAppleScript, NSTimer
from AppKit import NSApplication, NSApp, NSWorkspace
from Cocoa import *
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
from PyObjCTools import AppHelper

from rewind7am import rewindTime

DEBUG_APP = False
DEBUG_KEYSTROKE = False

def current_time():
  """
  Get a current UNIX timestamp.
  """
  return int(time.time())


def remove_non_ascii(s):
  """
  Dirty hack to replace non-ASCII characters in a string with spaces
  """
  if s is None:
    return None
  return ''.join(c if ord(c) < 128 else ' ' for c in s)


class AppDelegate(NSObject):

  def applicationDidFinishLaunching_(self, note):
    mask = NSKeyDownMask
    NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, self.event_sniffer.event_handler)
    NSEvent.addLocalMonitorForEventsMatchingMask_handler_(mask, self.event_sniffer.event_handler)

  def applicationActivated_(self, note):
    app =  note.userInfo().objectForKey_('NSWorkspaceApplicationKey')
    self.event_sniffer.set_active_app(app.localizedName())

  def screenSleep_(self, note):
    self.event_sniffer.screen_sleep_handler()

  def writeActiveApp_(self, timer):
    if DEBUG_APP:
      print 'Got active app callback at %d' % current_time()
    self.event_sniffer.write_active_app()


class EventSniffer:
  
  def __init__(self, options):
    self.options = options
    self.current_app = None
    self.last_app_logged = None
    self.init_chrome_tab_script()
    
  def init_chrome_tab_script(self):
    self.chrome_tab_script = NSAppleScript.alloc().initWithSource_(
      """
      tell application "Google Chrome"
        get URL of active tab of first window
      end tell
      """)

  def start_test_timer(self):
    NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
        1,
        self.delegate,
        'timerCallback:',
        None,
        True)
    
  def run(self):
    NSApplication.sharedApplication()
    self.delegate = AppDelegate.alloc().init()
    self.delegate.event_sniffer = self

    NSApp().setDelegate_(self.delegate)

    self.workspace = NSWorkspace.sharedWorkspace()
    nc = self.workspace.notificationCenter()

    # This notification needs OS X v10.6 or later
    nc.addObserver_selector_name_object_(
        self.delegate,
        'applicationActivated:',
        'NSWorkspaceDidActivateApplicationNotification',
        None)

    nc.addObserver_selector_name_object_(
        self.delegate,
        'screenSleep:',
        'NSWorkspaceScreensDidSleepNotification',
        None)

    # I don't think we need to track when the screen comes awake, but in case
    # we do we can listen for NSWorkspaceScreensDidWakeNotification

    NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
        self.options.active_window_time, self.delegate, 'writeActiveApp:',
        None, True)

    # Start the application. This doesn't return.
    AppHelper.runEventLoop()

  def set_active_app(self, app_name):
    self.current_app = remove_non_ascii(app_name)

  def event_handler(self, event):
    if event.type() == NSKeyDown:
      if DEBUG_KEYSTROKE:
        print 'Got keystroke in %s' % self.current_app
      with open(options.keystroke_raw_file, 'a') as f:
        f.write('\n')

  def screen_sleep_handler(self):
    self.current_app = '__LOCKEDSCREEN'

  def get_current_chrome_tab(self):
    """
    Execute the cached NSAppleScript to get the URL of active tab in Chrome.
    If Chrome is running but has no open tabs then None will be returned.
    Oddly enough if Chrome is not running then it will be started, and the
    tab name returned will be the default new tab URL.

    It's probably best to only call this if we know that Chrome is running.
    """
    res = self.chrome_tab_script.executeAndReturnError_(None)
    if res[0] is None:
      return None
    return str(res[0].stringValue())
  
  def get_current_window_name(self):
    options = kCGWindowListOptionOnScreenOnly
    window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in window_list:
      try:
        if window['kCGWindowOwnerName'] == self.current_app:
          window_name = window['kCGWindowName']
          return window_name
      except KeyError:
        pass
    return None

  def write_active_app(self):
    if self.current_app is not None:
      window_name = self.get_current_window_name()
      window_name = remove_non_ascii(window_name)
      if self.current_app == 'Google Chrome':
        window_name = self.get_current_chrome_tab()
        window_name = remove_non_ascii(window_name)
      if window_name is None or len(window_name) == 0:
        name_to_log = self.current_app
      else:
        name_to_log = '%s :: %s' % (self.current_app, window_name)
      if name_to_log != self.last_app_logged:
        self.last_app_logged = name_to_log
        s = '%d %s' % (current_time(), name_to_log)
        if DEBUG_APP:
          print s
        # substitute the rewound time to the window file pattern and write
        fname = self.options.active_window_file % (rewindTime(current_time()), )
        with open(fname, 'a') as f:
          f.write('%s\n' % s)

if __name__ == '__main__':
  option_list = [
      make_option('--pid_file',
                  action='store',
                  dest='pid_file',
                  default=None,
                  help='Required.'),
        make_option('--keystroke_raw_file',
                  action='store',
                  dest='keystroke_raw_file',
                  default=None,
                  help='Required.'),
      make_option('--active_window_file',
                  action='store',
                  dest='active_window_file',
                  default=None,
                  help='Required.'),
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

