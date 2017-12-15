import urllib
from mimetypes import MimeTypes

def response_telu():
	for filename in os.listdir(os.curdir):
		if (filename == "images.jpeg"):
			# path = os.getcwd()+"/"+filename
			mime = MimeTypes()
			# mime_type = mime.guess_type("http_server.png")
			url = urllib.pathname2url(filename)
			mime_type = mime.guess_type(url)
			ctype = mime_type[0]
			break

	file = open('images.jpeg','r').read()
	panjang = len(file)

	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: {}\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(ctype, panjang, file)

	return hasil