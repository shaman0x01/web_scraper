import sys,socket,optparse,requests
from bs4 import BeautifulSoup

class Server:
    def __init__(self, port):
        self.host = '127.0.0.1'
        self.port = port

    def listen(self):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.bind((self.host,self.port))
        listener.listen(0)
        print("[+] Waiting for Incoming Connection")
        self.connection,address = listener.accept()
        print("[+] Got a Connection from " + str(address))

    def receive(self):
    	data = ""
    	while True:
    		try:
    			data = data + self.connection.recv(1024).decode()
    			return data
    		except ValueError:
    			continue

    def send(self, data):
        self.connection.send(data.encode())

    def scrape_page(self, webpage):
    	page = requests.get(webpage)
    	soup = BeautifulSoup(page.content, 'html.parser')
    	p_elems = soup.findAll('p')
    	p_count = 0
    	for node in p_elems:
    		if not node.findChildren():
    			p_count += 1
    	img_elems = soup.findAll('img')
    	img_count = len(img_elems)
    	result = "Count of img tags: " + str(img_count) + "\nCount of leaf paragragh tags: " + str(p_count)
    	return result


    def run(self):
    	self.listen()
    	received_data = self.receive()
    	print("[+] Scraping web page...")
    	result = self.scrape_page(received_data)
    	self.send(str(result))
    	print("[+] Done!")


class Client:

	def connect(self, host, port):
		self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((host, port))

	def receive(self):
		data = ""
		while True:
			try:
				data = data + self.connection.recv(1024).decode()
				return data
			except ValueError:
				continue
	
	def send_to_scrape(self, webpage):
		self.connection.send(webpage.encode())
		received_data = self.receive()
		print(received_data)

def main():
	parser = optparse.OptionParser()
	parser.add_option("-p", metavar="PORT", type= int, help="Port on which server listens")
	if sys.argv[1] == "client":
		parser.add_option("--host", dest = "host", help="Ip address of server")
		parser.add_option("--webpage", dest = "webpage", help="Webpage url to scrape")
	(options,arguments) = parser.parse_args()
	if sys.argv[1] == "client":
		client = Client()
		client.connect(options.host, options.p)
		client.send_to_scrape(options.webpage)
	else:
		server = Server(options.p)
		server.run()

if __name__=="__main__":
	main()