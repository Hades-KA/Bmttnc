import tkinter as tk
from tkinter import ttk, messagebox
from hashlib import md5, sha256
from Crypto.Hash import SHA3_256, BLAKE2b

def calculate_hash(algorithm, text):
    try:
        if algorithm == "MD5":
            return md5(text.encode('utf-8')).hexdigest()
        elif algorithm == "SHA-256":
            return sha256(text.encode('utf-8')).hexdigest()
        elif algorithm == "SHA-3":
            sha3_hash = SHA3_256.new()
            sha3_hash.update(text.encode('utf-8'))
            return sha3_hash.hexdigest()
        elif algorithm == "Blake2":
            # Fixed parameter from digest_size to digest_bits
            blake2_hash = BLAKE2b.new(digest_bits=512)
            blake2_hash.update(text.encode('utf-8'))
            return blake2_hash.hexdigest()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate hash: {e}")
        return None

def on_calculate():
    text = input_text.get()
    algorithm = algorithm_combobox.get()
    if not text:
        messagebox.showwarning("Warning", "Please enter text to hash.")
        return
    if not algorithm:
        messagebox.showwarning("Warning", "Please select a hashing algorithm.")
        return
    hash_result = calculate_hash(algorithm, text)
    if hash_result:
        result_text.set(hash_result)

# Create the UI
root = tk.Tk()
root.title("Hashing Application")

# Input text label and entry
tk.Label(root, text="Enter text to hash:").pack(pady=5)
input_text = tk.Entry(root, width=50)
input_text.pack(pady=5)

# Algorithm selection
tk.Label(root, text="Select hashing algorithm:").pack(pady=5)
algorithm_combobox = ttk.Combobox(root, values=["MD5", "SHA-256", "SHA-3", "Blake2"], state="readonly")
algorithm_combobox.pack(pady=5)

# Calculate button
calculate_button = tk.Button(root, text="Calculate Hash", command=on_calculate)
calculate_button.pack(pady=10)

# Result label
tk.Label(root, text="Hash result:").pack(pady=5)
result_text = tk.StringVar()
result_label = tk.Entry(root, textvariable=result_text, width=150, state="readonly")
result_label.pack(pady=5)

# Start the UI loop
root.mainloop()
