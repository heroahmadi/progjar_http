import asyncore
import socket
import sys
import threading


#balba;a
def response_teks():
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 7\r\n" \
		"\r\n" \
		"PROGJAR"
	return hasil

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


class ClientHandler(asyncore.dispatcher):
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock=sock)
        self.request_message = ""
	self.reply_message=""
	return
    def handle_write(self):
	pass
    def handle_close(self):
	pass
     #fungsi melayani client
    def handle_read(self):
        data = self.recv(64)
        data = bytes.decode(data)
        self.request_message = self.request_message+data
        if (self.request_message[-4:]=="\r\n\r\n"):
            baris = self.request_message.split("\r\n")
	    baris_request = baris[0]
	    print baris_request
		
	    a,url,c = baris_request.split(" ")
	       
	    if (url=='/favicon.ico'):
		  respon = response_icon()
	    elif (url=='/doc'):
		  respon = response_dokumen()
	    elif (url=='/coba'):
		  respon = response_redirect()
	    else:
		  respon = response_gambar()
            self.request_message = ""
	    self.send(respon)
	    self.close()



class WebServer(asyncore.dispatcher):
    def __init__(self, host, port):
	asyncore.dispatcher.__init__(self)
	self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	self.set_reuse_addr()
	self.bind((host, port))
	self.listen(5)
    def handle_connect(self):
	pass
    def handle_expt(self):
	self.close()
    def handle_read(self):
	pass
    def handle_write(self):
	pass
    def handle_close(self):
	pass
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            koneksi_client, alamat_client = pair
            print 'Incoming connection from %s' % repr(alamat_client)
            ClientHandler(koneksi_client)        
	    #koneksi_client.send('haha')
	    #koneksi_client.close()
	    #s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
	    #s.start()

server = WebServer('localhost', 8080)
asyncore.loop()

