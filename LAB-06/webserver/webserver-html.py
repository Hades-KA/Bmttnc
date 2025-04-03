import socket
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script

def handle_request(client_socket, request_data):
    if "GET /admin" in request_data:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        admin_path = os.path.join(BASE_DIR, "admin.html")
        if os.path.exists(admin_path):
            with open(admin_path, "r") as file:
                response += file.read()
        else:
            response += "<h1>404 Not Found</h1><p>admin.html not found.</p>"
    else:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        index_path = os.path.join(BASE_DIR, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r") as file:
                response += file.read()
        else:
            response += "<h1>404 Not Found</h1><p>index.html not found.</p>"
    
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    print("Server listening on port 8080...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        request_data = client_socket.recv(1024).decode('utf-8')
        handle_request(client_socket, request_data)

if __name__ == '__main__':
    main()