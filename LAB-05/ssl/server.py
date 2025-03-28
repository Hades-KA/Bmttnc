import socket
import ssl
import threading
# Server information
server_address = ('localhost', 12345)
# List of connected clients
clients = []
def handle_client(client_socket):
    # Add client to the list
    clients.append(client_socket)
    print("Đã kết nối với:", client_socket.getpeername())
    try:
        # Receive and send data
        while True:         
            data = client_socket.recv(1024)
            if not data:
                break
            # Print received message
            print("Nhận:", data.decode('utf-8'))
            # Send data to all other clients
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except:
                        if client in clients:
                            clients.remove(client)
    except:
        if client_socket in clients:
            clients.remove(client_socket)
    finally:
        print("Đã ngắt kết nối:", client_socket.getpeername())
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
# Create socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server đang chờ kết nối...")
# Listen for connections
while True:
    client_socket, client_address = server_socket.accept()
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    # Update the paths to the certificate and key files
    # Ensure these files exist or generate them using OpenSSL:
    # Command to generate:
    # openssl req -new -x509 -days 365 -nodes -out server-cert.crt -keyout server-key.key
    context.load_cert_chain(certfile="./LAB-05/ssl/certificates/server-cert.crt",
                            keyfile="./LAB-05/ssl/certificates/server-key.key")

    # Establish SSL connection
    ssl_socket = context.wrap_socket(client_socket, server_side=True)
    # Start a thread for each client
    client_thread = threading.Thread(target=handle_client, args=(ssl_socket,)) 
    client_thread.start()