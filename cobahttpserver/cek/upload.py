import os
import commands
import cgi, cgitb

cgitb.enable()
print "Content-Type: text/html"
print
print 'start!'
form = cgi.FieldStorage()
filedata = form['upload']
if filedata.filename:

    # strip leading path from file name
    # to avoid directory traversal attacks
    fn = os.path.basename(filedata.filename)
    open('files/' + fn, 'wb').write(filedata.file.read())
    message = 'The file "' + fn + '" was uploaded successfully'

else:
    message = 'No file was uploaded'

print """\
<html><body>
<p>%s</p>
</body></html>
""" % (message,)

