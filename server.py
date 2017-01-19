#  coding: utf-8
import os
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Michele Paulichuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    # send 405 error message for HTTP methods not handled
    def send405(self):
	    #print("Sending 405 Method Not Allowed")
        header = "HTTP/1.1 405 Method Not Allowed \r\n"
        close = "Connection: close \r\n\r\n"
        self.request.sendall(header + close)

    # send 404 error message for any path that does not exist
    def send404(self):
	    #print("Sending 404 Not Found")
        header = "HTTP/1.1 404 Not Found \r\n"
        close = "Connection: close \r\n\r\n"
        self.request.sendall(header + close)
    # send 200 Ok message and server up the requested file
    def send200(self, path) :
	    #print("Sending 200 OK")
        header = "HTTP/1.1 200 OK \r\n"

        # Get mimeType of file to serve
        if (path.lower().endswith(".html")):
            mimeType = "Content-Type: text/html \r\n"
        elif (path.lower().endswith(".css")):
            mimeType = "Content-Type: text/css \r\n"
        else:
            self.send404()
        
        # Try to server the request back
        try:
            print("Sending data at: %s" % path)
            data = open(path).read()
            close = "Connection: close \r\n\r\n"
            self.request.sendall(header + mimeType + close + data)
        except:
            self.send404()


    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        requestData = self.data.split(" ")
        requestMethod = requestData[0]

        # Check if method is a valid method to handle
        if (requestMethod == "GET"):
            #Grabbing absolute path of request to prevent retrieval of files outside application
            requestedFileLoc = os.path.abspath(requestData[1])
            currentDir = os.getcwd()
            fullPath = currentDir + "/www" + requestedFileLoc

            # check if path exists
            if (os.path.exists(fullPath)):
                if (not requestedFileLoc.endswith(tuple([".html",".css"]))):
                    fullPath += "/index.html"

                self.send200(fullPath)
            else:
                self.send404()
        else:
            self.send405()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
