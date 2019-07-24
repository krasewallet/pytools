#coding:utf-8
import http.server
import os
import urllib.parse
import html
import io
import shutil
import socketserver

class RequestHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    path = os.path.dirname(__file__)
    for name in urllib.parse.unquote(self.path).split('/'):
      path = os.path.join(path,name)
    if os.path.isdir(path):
      f = self.list_dir(path)
      shutil.copyfileobj(f, self.wfile)
      f.close()
    else:
      f = self.show_file(path)
      shutil.copyfileobj(f, self.wfile)
      f.close()
  def do_POST(self):
    pass
  def show_file(self,file):
    try:
      f = open(file,'rb')
      self.send_response(200)
      self.send_header("Content-type", "application/octet-stream")
      self.send_header("Content-Length", os.fstat(f.fileno())[6])
      self.end_headers()
    except Exception as e:
      self.send_error(404,str(e))
    return f
  def list_dir(self, folder):
    files = os.listdir(folder)
    f = io.BytesIO()
    html_list = ""
    for name in files:
      fullname = os.path.join(folder, name)
      displayname = linkname = os.path.basename(fullname)
      # Append / for directories or @ for symbolic links
      if os.path.isdir(fullname):
          displayname = name + "/"
          linkname = name + "/"
      if os.path.islink(fullname):
          displayname = name + "/"
      # Note: a link to a directory displays with @ and links with /
      html_list += f'''
      <li><a href="{urllib.parse.quote(linkname)}">{html.escape(displayname)}</a></li>
      '''
    template = f'''
    <!DOCTYPE html>
    <html>
    <head>
    <title>SimpleFileServer</title>
    </head>
    <body>
      <form ENCTYPE="multipart/form-data" method="post">
        <input name="file" type="file"/><input type="submit" value="upload"/>
      </form>
      <ul>
        {html_list}
      </ul>
    </body>
    </html>
    '''
    f.write(template.encode())
    length = f.tell()
    f.seek(0)
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.send_header("Content-Length", str(length))
    self.end_headers()
    return f
if __name__ == "__main__":
  class ThreadingServer(socketserver.ThreadingMixIn,http.server.HTTPServer):
    pass
  server = ThreadingServer(("",8080),RequestHandler)
  server.serve_forever()