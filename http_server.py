import datetime
import codecs
import socket
import sys
import threading
import os
import shutil
import cgi, cgitb
import urllib
from mimetypes import MimeTypes

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#proses binding
if len(sys.argv) == 1:
	port = 10000
else:
	port = int(sys.argv[1])
server_address = ('localhost', port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)

def get_input(mydir):
	mydir = mydir.split('Cookie')
	mydir = mydir[1].split('input=')
	mydir = mydir[1].split('&')[0]
	
	return mydir

def response_no1(url):
	url = url.split('?dir=')
	if len(url) == 1:
		directory = os.curdir
	else:
		if url[1] == '':
			directory = os.curdir
		else:
			directory = url[1]
	
	fullpath = os.getcwd() + '/' + directory
	fullpath = fullpath.replace('/.', '')
	
	if os.path.isfile(fullpath):
		return response_telu(directory)
	
	files = os.listdir(directory)
	if directory == '.':
		current = ''
	else:
		current = directory
		current += '/'
	isi = '<h1>Current folder : /'+current+'</h1>'
	isi += '<p>Folder Action :</p>'
	isi += '<p><a href="/6">Hapus Folder</a>&nbsp&nbsp&nbsp&nbsp<a href="/5?curdir='+current+'">Buat Folder</a>&nbsp&nbsp&nbsp&nbsp<a href="/2">Upload file disini</a></p>'
	isi += '<hr>'
	
	for f in files:
		isi += '<div><a href="/1?dir='+current+f+'">'+f+'</a>&nbsp&nbsp&nbsp&nbsp'
		isi += '<form><input type="button" value="Pindah" onclick="window.location.href=\'/7?file='+fullpath+'/'+f+'\'"/><input type="button" value="Hapus" onclick="window.location.href=\'/4?file='+fullpath+'/'+f+'\'"/></form></div>'

	panjang = len(isi)

	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(panjang, isi)

	return hasil

def response_no5(url):
	mydir = ("<form method=\"POST\" action=\"\"><input type=\"text\" name=\"input\" id=\"folder\" placeholder=\"Nama Folder\" /><input type=\"hidden\" name=\"countryxsz\" value=\"Norway\"><input type=\"submit\" value=\"submit\"/> ")
	panjang = len(mydir)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, mydir)
	return hasil

def buat_dir(url, data):
	data = get_input(data)
	url = url.split('?curdir=')
	print "CURDIR MAMEEEEN", url[1]
	print "DATA MAMEEEEN", data
	
	fullpath = os.getcwd() + '/' + url[1] + data
	if not os.path.exists(fullpath):
		os.makedirs(fullpath)
		data = 'sukses'
	else:
		data = 'gagal'
			
	panjang = len(data)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, data)
	return hasil
	
def response_telu(namafile):

	isi = ''

	for filename in os.listdir(os.curdir):
		if (filename == namafile):
			# path = os.getcwd()+"/"+filename
			mime = MimeTypes()
			# mime_type = mime.guess_type("http_server.png")
			url = urllib.pathname2url(filename)
			mime_type = mime.guess_type(url)
			ctype = mime_type[0]
			break

	file = open(namafile,'r').read()
	panjang = len(file)

	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: {}\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(ctype, panjang, file)

	return hasil

def response_no2():
	isi = "<form action=\"input\" method=\"post\" enctype=\"multipart/form-data\"><input type=\"file\" name=\"fileToUpload\" id=\"fileToUpload\"><input type=\"hidden\" name=\"countryxsz\" value=\"Norway\"><input type=\"submit\" value=\"Submit\"></form>"

	panjang = len(isi)
	
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(panjang, isi)

	return hasil

def response_input_no2(req):
	#formData = cgi.FieldStorage()
	#print formData
	a,req=req.split("name=\"fileToUpload\"; ")
	#req,a,c=req.split(" -----------------------------")
	req=req.split("-----------------------------")	
	b=req[0].split("Content-Type: ")
	#get isi
	x=b[1].split("\n\r")
	print len(x)
	print "menghilangkan content type"
	print x
	#menciptakan judul
	now = datetime.datetime.now()
	now = str(now)
	now = now.replace(".","")
	now = now.replace(" ","")
	a=b[0].split("Content-Type: ")
	flnm=a[0].split("filename=\"")
	flnm=flnm=flnm[1].split("\"")
	flnm=now+flnm[0]
	print flnm
	file = open(flnm,"w")
	for xy in range(len(x)):
		if xy!=0:
			print "print"
			file.write(x[xy])
	file.close()
	#b[1]isi file
	msg="Sukses"
	panjang = len(msg)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(panjang, msg)
	return hasil

def response_no6():
	mydir= ("<form method=\"POST\" action=\"/hapusdir\"><input type=\"text\" name=\"input\" id=\"folder\" placeholder=\"Masukkan Folder yang akan dihapus\" /><input type=\"hidden\" name=\"countryxsz\" value=\"Norway\"><input type=\"submit\" value=\"submit\"/> ")
	panjang = len(mydir)

	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, mydir)
	return hasil

def response_no7(url):
	mydir = ("<form method=\"POST\" action=\"\"><input type=\"text\" name=\"input\" id=\"folder\" placeholder=\"Folder Tujuan\" /><input type=\"hidden\" name=\"countryxsz\" value=\"Norway\"><input type=\"submit\" value=\"submit\"/> ")
	panjang = len(mydir)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, mydir)
	return hasil

def hapus_dir(mydir):
	mydir = get_input(mydir)
	path = os.getcwd()
	try:
		shutil.rmtree(path+'/'+mydir)
		isi = 'Sukses'
	except OSError, e:
		print ("Error: %s - %s." % (e.filename,e.strerror))
		isi = e.strerror

	panjang = len(isi)
	
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, isi)
	return hasil
	
def hapus_file(filepath):
	filepath = filepath.split('?file=')[1]
	try:
		os.remove(filepath)
		isi = 'Sukses'
	except OSError, e:
		print ("Error: %s - %s." % (e.filename,e.strerror))
		isi = e.strerror

	panjang = len(isi)
	
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, isi)
	return hasil

def pindah(url, data):
	dest = get_input(data)
	thefile = url.split('?file=')[1]
	
	if os.path.isfile(thefile):
		dest = os.getcwd() + '/' + urllib.unquote(dest).decode('utf8')
		os.rename(thefile, dest)
	elif os.path.isdir(thefile):
		dest = os.getcwd() + '/' + urllib.unquote(dest).decode('utf8') + '/'
		shutil.move(thefile, dest)
	
	data = 'sukses'
	
	panjang = len(data)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, data)
	return hasil
	
"""
def response_no8():
	mydir= ("<input type=\"text\" name=\"input\" id=\"folder\" placeholder=\"Masukkan Folder yang akan dihapus\" /> <input type=\"submit\" value=\"submit\"/> ")
	panjang = len(mydir)

	try:
		shutil.rmtree(mydir)
	except OSError, e:
		print ("Error: %s - %s." % (e.filename,e.strerror))

	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, mydir)
	return hasil
"""

def response_gambar():
	filegambar = open('gambar.png','r').read()
	panjang = len(filegambar)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: image/png\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil

def response_icon():
	filegambar = open('myicon.png','r').read()
	panjang = len(filegambar)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: image/png\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil

def response_dokumen():
	filedokumen = open('dok.pdf','r').read()
	panjang = len(filedokumen)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: application/pdf\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filedokumen)
	return hasil

def response_redirect():
	hasil = "HTTP/1.1 301 Moved Permanently\r\n" \
		"Location: {}\r\n" \
		"\r\n"  . format('http://www.its.ac.id')
	return hasil


#fungsi melayani client
def layani_client(koneksi_client,alamat_client):
<<<<<<< HEAD
    try:
       print >>sys.stderr, 'ada koneksi dari ', alamat_client
       request_message = ''
       while True:
           data = koneksi_client.recv(64)
	   data = bytes.decode(data)
           request_message = request_message+data
	   if (request_message[-4:]=="\r\n\r\n"):
		break

       baris = request_message.split("\r\n")
       baris_request = baris[0]
       print baris_request
 	
       a,url,c = baris_request.split(" ")
       
       if (url=='/favicon.ico'):
          respon = response_icon()
       elif (url=='/doc'):
	  respon = response_dokumen()
       elif (url=='/teks'):
          respon = response_teks()
       elif (url=='/1'):
		  respon = response_no1()
       elif (url=='/7'):
		  respon = response_no7()
       else:
          respon = response_gambar()

       koneksi_client.send(respon)
    finally:
        # Clean up the connection
        koneksi_client.close()
=======
	try:
		print >>sys.stderr, 'ada koneksi dari ', alamat_client
		request_message = ''
		data = koneksi_client.recv(32)
		data = bytes.decode(data)
		print data
		request_message = request_message+data
		
		if("GET" in data):
			print "Method Get"
			while True:
				data = koneksi_client.recv(32)
				data = bytes.decode(data)
				print data
				request_message = request_message+data
				if (request_message[-4:]=="\r\n\r\n"):
					break
		elif("POST" in data):
			print "Method Post"
			while True:
				data = koneksi_client.recv(4096)
				request_message = request_message+data
				if ("countryxsz" in data):
					break
		
		print request_message
		baris = request_message.split("\r\n")
		baris_request = baris[0]
		print baris_request		
		a,url,c = baris_request.split(" ")
		print url
		if (url=='/favicon.ico'):
			respon = response_icon()
		elif (url=='/doc'):
			respon = response_dokumen()
		elif (url=='/teks'):
			respon = response_teks()
		elif (url[:2]=='/1'):
			respon = response_no1(url)
		elif (url=='/3'):
			respon = response_telu()
		elif (url=='/2'):
			respon = response_no2()
		elif (url=='/6'):
			respon = response_no6()
		elif ("POST" in a and url[:2]=='/7'):
			respon = pindah(url, request_message)
		elif (url[:2]=='/7'):
			respon = response_no7(url)
		elif (url[:2]=='/4'):
			respon = hapus_file(url)
		elif ("POST" in a and url[:2]=='/5'):
			respon = buat_dir(url, request_message)
		elif (url[:2]=='/5'):
			respon = response_no5(url)
		elif ("POST" in a and url=='/hapusdir'):
			respon = hapus_dir(request_message)
		elif ("POST" in a and url=='/input'):
			#formData = cgi.FieldStorage()
			#name=formData.getvalue('name_field')
			#print "xxxx"
			#print name
			#print formData
			#print "xxxx"
			respon = response_input_no2(request_message)
		elif (url=='/6'):
			respon = response_no6()
		elif (url=='/8'):
			respon = response_no8()
		else:
			respon = response_gambar()

		koneksi_client.send(respon)
	finally:
		# Clean up the connection
		koneksi_client.close()
>>>>>>> master


while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	koneksi_client, alamat_client = sock.accept()
	s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
	s.start()


