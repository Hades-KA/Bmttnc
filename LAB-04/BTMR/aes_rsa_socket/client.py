from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import hashlib
# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
# Generate RSA key pair
client_key = RSA.generate(2048)
# Receive server's public key
server_public_key = RSA.import_key(client_socket.recv(2048))
# Send client's public key to the server
client_socket.send(client_key.publickey().export_key(format='PEM'))
# Receive encrypted AES key from the server
encrypted_aes_key = client_socket.recv(2048)
# Decrypt the AES key using client's private key
cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)
# Function to encrypt message
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext
# Function to decrypt message
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()
# Function to handle sending messages from the UI
def send_message():
    message = message_entry.get()
    if message:
        encrypted_message = encrypt_message(aes_key, message)
        client_socket.send(encrypted_message)
        chat_window.insert(tk.END, f"You: {message}\n")
        message_entry.delete(0, tk.END)
        if message == "exit":
            client_socket.close()
            root.quit()
# Function to update the chat window with received messages
def update_chat_window(decrypted_message):
    chat_window.insert(tk.END, f"Received: {decrypted_message}\n")
# Modified receive_messages to update the UI
def receive_messages():
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            update_chat_window(decrypted_message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
# Start the receiving thread
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()
# Create the UI
root = tk.Tk()
root.title("AES-RSA Chat Client")
# Chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=50)
chat_window.pack(padx=10, pady=10)
chat_window.config(state=tk.NORMAL)
# Message entry
message_entry = tk.Entry(root, width=40)
message_entry.pack(side=tk.LEFT, padx=10, pady=10)
# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)
# Start the UI loop
root.mainloop()