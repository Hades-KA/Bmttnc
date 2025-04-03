import tkinter as tk
from tkinter import messagebox, scrolledtext
import socket
import ssl
import threading

class SSLClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSL Client")
        self.ssl_socket = None

        # Server address input
        tk.Label(root, text="Server Address:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_server = tk.Entry(root, width=30)
        self.entry_server.grid(row=0, column=1, padx=10, pady=5)
        self.entry_server.insert(0, "localhost")

        # Server port input
        tk.Label(root, text="Port:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_port = tk.Entry(root, width=10)
        self.entry_port.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.entry_port.insert(0, "12345")

        # Connect button
        self.btn_connect = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.btn_connect.grid(row=2, column=0, columnspan=2, pady=10)

        # Message input
        tk.Label(root, text="Message:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_message = tk.Entry(root, width=50)
        self.entry_message.grid(row=3, column=1, padx=10, pady=5)

        # Send button
        self.btn_send = tk.Button(root, text="Send", command=self.send_message, state=tk.DISABLED)
        self.btn_send.grid(row=4, column=0, columnspan=2, pady=10)

        # Received messages display
        tk.Label(root, text="Received Messages:").grid(row=5, column=0, padx=10, pady=5)
        self.text_received = scrolledtext.ScrolledText(root, width=60, height=15, state=tk.DISABLED)
        self.text_received.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def connect_to_server(self):
        server_address = self.entry_server.get()
        try:
            port = int(self.entry_port.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")
            return

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.verify_mode = ssl.CERT_NONE
            self.ssl_socket = context.wrap_socket(client_socket, server_hostname=server_address)
            self.ssl_socket.connect((server_address, port))
            self.btn_send.config(state=tk.NORMAL)
            self.btn_connect.config(state=tk.DISABLED)
            threading.Thread(target=self.receive_messages, daemon=True).start()
            messagebox.showinfo("Success", "Connected to server!")
        except ConnectionRefusedError:
            messagebox.showerror("Error", "Connection refused! Ensure the server is running.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def send_message(self):
        message = self.entry_message.get()
        if not message:
            messagebox.showwarning("Warning", "Message cannot be empty!")
            return
        try:
            self.ssl_socket.send(message.encode("utf-8"))
            self.entry_message.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    def receive_messages(self):
        try:
            while True:
                data = self.ssl_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                self.text_received.config(state=tk.NORMAL)
                self.text_received.insert(tk.END, f"Server: {message}\n")
                self.text_received.config(state=tk.DISABLED)
        except Exception as e:
            self.text_received.config(state=tk.NORMAL)
            self.text_received.insert(tk.END, f"Connection closed: {e}\n")
            self.text_received.config(state=tk.DISABLED)
        finally:
            self.ssl_socket.close()
            self.ssl_socket = None
            self.btn_send.config(state=tk.DISABLED)
            self.btn_connect.config(state=tk.NORMAL)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SSLClientApp(root)
    root.mainloop()
