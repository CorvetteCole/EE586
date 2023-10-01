from socket import *
from pathlib import Path

CACHE_DIR = Path('cache')
CACHE_DIR.mkdir(exist_ok=True)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.bind(('', 8888))
clientSocket.listen(1)

print('Ready to proxy...')

# Server should be up and running and listening to the incoming connections
while True:
    # Set up a new connection from the client
    connectionSocket, addr = clientSocket.accept()

    # Receives the request message from the client
    message = connectionSocket.recv(1024)

    # Extract the path of the requested object from the message
    # The path is the second part of HTTP header, identified by [1]
    filename = message.split()[1].decode()[1:]

    # Check if file is in cache
    if (CACHE_DIR / filename).exists():
        print(f'Serving {filename} from cache...')
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        with open(CACHE_DIR / filename, 'rb') as f:
            connectionSocket.send(f.read())
    else:
        print(f'Fetching {filename} from web server...')
        # connect to web server running on localhost on port 6789
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect(('localhost', 6789))
        serverSocket.send(message)
        response = serverSocket.recv(1024)
        print(f'Received response from web server for {filename}')
        connectionSocket.send(response)
        # if the response was a 200 OK, cache the file
        if response.split()[1] == b'200':
            with open(CACHE_DIR / filename, 'wb') as f:
                print(f'Caching {filename}...')
                f.write(response)
    connectionSocket.close()

