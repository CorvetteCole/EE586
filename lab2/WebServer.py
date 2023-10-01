# Import socket module
from socket import *

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', 6789))
serverSocket.listen(1)
print('Ready to serve...')

# Server should be up and running and listening to the incoming connections
try:
    while True:
        # Set up a new connection from the client
        connectionSocket, addr = serverSocket.accept()

        # If an exception occurs during the execution of try clause
        # the rest of the clause is skipped
        # If the exception type matches the word after except
        # the except clause is executed
        try:
            # Receives the request message from the client
            message = connectionSocket.recv(1024)

            # Extract the path of the requested object from the message
            # The path is the second part of HTTP header, identified by [1]
            filename = message.split()[1]

            # Because the extracted path of the HTTP request includes
            # a character '\', we read the path from the second character
            with open(filename[1:], 'rb') as f:
                print(f'Serving {filename[1:]}')
                # Send the HTTP response header line to the connection socket
                connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                # send the file content to the client
                connectionSocket.send(f.read())
                # Close the client connection socket
                connectionSocket.close()

        except IOError:
            # Send HTTP response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

            # Close the client connection socket
            connectionSocket.close()
except:
    serverSocket.close()
