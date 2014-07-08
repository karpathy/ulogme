import SocketServer
import SimpleHTTPServer
import sys
import cgi
import os

# Port settings
IP = ""
if len(sys.argv) > 1:
  PORT = int(sys.argv[1])
else:
  PORT = 8123

# serve render/ folder, not current folder
rootdir = os.getcwd()
os.chdir('render')

# Custom handler
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def do_GET(self):
    # intercept special paths
    if self.path=='/note':
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write('OK')
    else:
      # default behavior
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self) 

  def do_POST(self):
    form = cgi.FieldStorage(
      fp = self.rfile,
      headers = self.headers,
      environ = {'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type']})
    result = 'NOT_UNDERSTOOD'

    if self.path == '/refresh':
      # recompute jsons. We have to pop out to root from render. It's a little ugly
      refresh_time = form.getvalue('time')
      os.chdir(rootdir) # pop out
      if refresh_time != '0':
        os.system('python export_events.py ' + refresh_time)
      else:
        os.system('python export_events.py') # reload all events
        
      os.chdir('render') # pop back to render directory
      result = 'OK'
      
    if self.path == '/addnote':
      # add note at specified time and refresh
      note = form.getvalue('note')
      note_time = form.getvalue('time')
      print 'adding note %s at time %s.' % (note, note_time)
      os.chdir(rootdir) # pop out
      with open("logs/notes.txt", "a") as myfile:
        myfile.write(note_time + ' ' + note + '\n')
      os.system('python export_events.py ' + note_time) # recompute at this time
      os.chdir('render') # go back to render
      result = 'OK'
    
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    self.wfile.write(result)

httpd = SocketServer.ThreadingTCPServer((IP, PORT), CustomHandler)

print 'Serving ulogme, see it on http://localhost:' + `PORT`
httpd.serve_forever()

