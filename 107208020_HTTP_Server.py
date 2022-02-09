#server

# import the socket library provided by Python
# theoretically, you can only use the socket library to create an Internet server/client
# however, the socket library is a low-level library
# it may not easy to use socket library only to create complicated network-based apps

# if you are interested in all functions provided by Python, see this
# https://docs.python.org/3.7/library/socket.html

import socket

# As a server, we would like to serve multiple clients
# so we use one thread to serve one client
# threading is a python library that can spawn multiple threads in a single app (process)

import threading

# create socket instance
# socket.AF_INET is a constant value that indicates I want to use IP (Internet Protocol) as my L3 protocol
# socket.SOCK_STREAM is a constant value that indicates I want to use TCP as my L4 protocol

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ask the OS to bind the created socket to user-specified parameters: (IP, TCP port)
# the 1st parameter is the binded IP, the 2nd parameter is the binded port number
# So that when the OS receives a datagram, the OS knows how to demux the datagram to the corresponding application 

pars = ('127.0.0.1', 80) # you can change the server port to whatever you want
s.bind(pars)

# become a server socket
# it makes this python program waiting for receiving message
# listen() function has one parameter that limits how many clients can be connected to this server
# we set it to 5 without any reason
# you can change it to any number you want, as long as you have sufficient resources (computing, memory)

s.listen(5)


# a new thread is created for every new accepted client
# every new thread starts from the function below

def serveClient(clientsocket, address):
    
    # we need a loop to continuously receive messages from the client
    while True:
        # then receive at most 1024 bytes message and store these bytes in a variable named 'data'
        # you can set the buffer size to any value you like
        data = clientsocket.recv(1024).decode()
        #print("from client", data)

        if data:
            #print(data)
            data_list = data.split("\r\n")
            request = data_list[0]
            request_method = request.split(" ")[0]
            url = request.split(" ")[1][1:]
            if request_method == "GET":
                if url == "get.html":
                    clientsocket.send(b"<html><body>good.html</body></html>\r\n")
                elif url == "redirect.html":
                    clientsocket.send(b"HTTP/1.1 301 Moved Permanently\r\n")
                    clientsocket.send(b"Location: /get.html\r\n")
                elif url == "notfound.html":
                    clientsocket.send(b"HTTP/1.1 404 Not Found\r\n")
                    clientsocket.send(b"<html><body>404 Not Found</body></html>\r\n")
                else:
                    clientsocket.send(b"<html><body>\
                                             <form action=\"/post.html\" method=\"post\">\
                                                <label for=\"std_id\">Student ID = </label>\
                                                <input\
                                                    type=\"text\"\
                                                    name=\"id\"\
                                                    value=\"107208020\"\
                                                    placeholder=\"107208020\"\
                                                    style=\"display:inline-block;width:100px\"\
                                                    id=\"std_id\">\
                                                <input type=\"submit\" value=\"POST\">\
                                            </form>\
                                        </body></html>\r\n")
            elif request_method == "HEAD":
                if url == "head.html" or url == "head.html?":
                    clientsocket.send(b"HTTP/1.1 200 OK\r\n\r\n")
                    #clientsocket.send(b"<html><body>good.html</body></html>\r\n")
                    #print(request_method)
                    #print(data)
            elif request_method == "POST":
                content = data_list[-1]
                if url == "post.html":
                    clientsocket.send( b"<html><body>" + bytes(content.split("=")[-1].encode()) + b"</body></html>\r\n" )

            clientsocket.close()
            
            #non-persistent
            break 
            


# since at most we can serve many clients (5 in this example), we need a way to distinguish them 
# as mentioned in the class, TCP use 4-tuple (src IP, dst IP, src port, dst port) to distinguish a socket
# we use accept() function to confirm that we connect to the client socket
# and accept() function will return the client's socket instance and IP
# we need a loop to keep accepting new clients (until 5 clients are accepted)

while True:
    # accept a new client and get it's information
    (clientsocket, address) = s.accept()
    
    # create a new thread to serve this new client
    # after the thread is created, it will start to execute 'target' function with arguments 'args' 
    threading.Thread(target = serveClient, args = (clientsocket, address)).start()

    