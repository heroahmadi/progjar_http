import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
import zipfile
import cgitb

cgitb.enable()
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):

        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
        if ctype == 'multipart/form-data':
            print "file"
            # query = cgi.parse_multipart(self.rfile, pdict)
            r, info = self.deal_post_data()
            print r, info, "by: ", self.client_address
            f = StringIO()
            f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
            f.write("<html>\n<title>Upload Result Page</title>\n")
            f.write("<body>\n<h2>Upload Result Page</h2>\n")
            f.write("<hr>\n")
            if r:
                f.write("<strong>Success:</strong>")
            else:
                f.write("<strong>Failed:</strong>")
            f.write(info)
            f.write("<br><a href=\"%s\">back</a>" % self.headers['referer'])
            f.write("<hr><small>Powerd By: bones7456, check new version at ")
            f.write("<a href=\"http://li2z.cn/?s=SimpleHTTPServerWithUpload\">")
            f.write("here</a>.</small></body>\n</html>\n")
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
        else:
            length = int(self.headers['content-length'])
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            if postvars.get('hapusdir') is not None:
                s=os.getcwd()
                d=postvars['hapusdir']

                d=str(d)
                d=d.replace("[","")
                d=d.replace("]","")
                d=d.replace("'","")
                print d
                #s=s+"\\"+d#windows
		s=s+"/"+d#linux
                print s
                os.rmdir(s)
                print "Hapus Directory"
                print postvars['hapusdir']

            elif postvars.get('hapusfile') is not None:
                print "Hapus File"
                print postvars['hapusfile']


    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")


    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        print path
        if self.path.endswith('?download'):
            tmp_file = "tmp.zip"
            self.path = self.path.replace("?download", "")

            zip = zipfile.ZipFile(tmp_file, 'w')
            for root, dirs, files in os.walk(path):
                for file in files:
                    if os.path.join(root, file) != os.path.join(root, tmp_file):
                        zip.write(os.path.join(root, file))
            zip.close()
            path = self.translate_path(tmp_file)
        elif os.path.isdir(path):
            print "Benar"
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f


    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n")
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write("<hr>\n")
        f.write("<h2>Hapus Directory</h2>")
        f.write("<form method=\"post\">")
        f.write("<input name=\"hapusdir\"/>")
        f.write("</form>")
        f.write("<hr>\n")
        f.write("<h2>Hapus File</h2>")
        f.write("<form method=\"post\">")
        f.write("<input name=\"hapusfile\"/>")
        f.write("</form>")
        f.write("<hr>\n")
        f.write("<a href='%s'>%s</a>\n" % (self.path + "?download", 'Download Directory Tree as Zip'))
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f


    def translate_path(self, path):
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path


    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)


    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']


    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


def main(HandlerClass=SimpleHTTPRequestHandler, ServerClass=BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    main()
