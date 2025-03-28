from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText  # Import ScrolledText for scrollable text box

def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def perform_key_exchange():
    try:
        # Load server's public key
        with open("c:/Users/TRUONG HUU/Downloads/LAB-04/dh_key_pair/server_public_key.pem", "rb") as f:
            server_public_key = serialization.load_pem_public_key(f.read())
        parameters = server_public_key.parameters()
        private_key, public_key = generate_client_key_pair(parameters)
        shared_secret = derive_shared_secret(private_key, server_public_key)
        
        # Display the shared secret in the scrollable text box with prefix
        shared_secret_textbox.delete(1.0, tk.END)  # Clear previous content
        shared_secret_textbox.insert(tk.END, f"Shared Secret: {shared_secret.hex()}")
    except Exception as e:
        messagebox.showerror("Error", f"Key exchange failed: {e}")

# Create the UI
root = tk.Tk()
root.title("Diffie-Hellman Key Exchange")

# Instruction label
instruction_label = tk.Label(root, text="Click the button to perform key exchange:")
instruction_label.pack(pady=10)

# Perform key exchange button
exchange_button = tk.Button(root, text="Perform Key Exchange", command=perform_key_exchange)
exchange_button.pack(pady=10)

# Scrollable text box for shared secret
shared_secret_textbox = ScrolledText(root, wrap=tk.WORD, height=10, width=150)
shared_secret_textbox.pack(pady=10)

# Start the UI loop
root.mainloop()