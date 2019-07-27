#coding:utf-8
import http.server
import os
import urllib.parse
import html
import io
import shutil
import socketserver
import re

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
      if f:
        shutil.copyfileobj(f, self.wfile)
        f.close()

  def do_POST(self):
    path = os.path.dirname(__file__)
    for name in urllib.parse.unquote(self.path).split('/'):
      path = os.path.join(path,name)
    self.parseFormData(path)

    self.send_response(200)
    success = b'success'
    self.send_header("Content-type", "text/plain")
    self.send_header("Content-Length", str(len(success)))
    self.end_headers()
    self.wfile.write(success)

  def show_file(self,file):
    try:
      f = open(file,'rb')
      self.send_response(200)
      self.send_header("Content-type", "application/octet-stream")
      self.send_header("Content-Length", os.fstat(f.fileno())[6])
      self.end_headers()
      return f
    except Exception as e:
      self.send_error(404,str(e))
      
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
  
  def parseFormData(self,path):
    # 'multipart/form-data; boundary=----WebKitFormBoundary5iYS2bLq7sBRFNMk'
    mBoundary = re.findall(r'boundary=(.*)',self.headers['Content-Type'])
    remainbytes = int(self.headers['Content-length'])
    form = {}
    begin = False
    key = None
    value = None
    writter = None
    if mBoundary:
      boundary = mBoundary[0].encode('utf-8')
      while remainbytes > 0:
        line = self.rfile.readline()
        print(line)
        remainbytes -= len(line)
        if begin:
          if key and not value[b'value']:
              if value[b'file'] and not value[b'mime']:
                m = re.match(b'Content-Type: (.*)\r\n',line)
                value[b'mime'] = m.group(1)
              elif not writter:
                if value[b'file']:
                  writter = open(value[b'path'],'wb')
                else:
                  writter = io.BytesIO()
              elif not boundary in line:
                writter.write(line)

          if line.startswith(b'Content-Disposition:'):
            # b'Content-Disposition: form-data; name="file"; filename="&#26032;&#24314;&#25991;&#26412;&#25991;&#26723;.txt"\r\n'
            result = re.findall(b'\s(\w+)="(.*?)"',line)
            params = dict(result)
            key = params[b'name']
            value = {
              b'file': b'filename' in params,
              b'path': os.path.join(path,html.unescape(params[b'filename'].decode())) if b'filename' in params else None,
              b'mime': None,
              b'value': None
            }
          if boundary in line:
            if writter:
              writter.seek(-2,2)
              writter.truncate()
              value[b'value'] = b'' if value[b'file'] else writter.getvalue()
              writter.close()
            form.setdefault(key,value)
            begin = False
            key = None
            value = None
            writter = None
        if not begin and boundary in line:
          begin = True
      return form
if __name__ == "__main__":
  class ThreadingServer(socketserver.ThreadingMixIn,http.server.HTTPServer):
    pass
  server = ThreadingServer(("",8080),RequestHandler)
  server.serve_forever()