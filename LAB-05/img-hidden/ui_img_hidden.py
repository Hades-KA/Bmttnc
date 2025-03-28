import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def encode_image(image_path, message):
    try:
        img = Image.open(image_path)
        width, height = img.size
        binary_message = ''.join(format(ord(char), '08b') for char in message) + '11111111111111110'
        data_index = 0

        for row in range(height):
            for col in range(width):
                pixel = list(img.getpixel((col, row)))
                for color_channel in range(3):
                    if data_index < len(binary_message):
                        pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1
                img.putpixel((col, row), tuple(pixel))
                if data_index >= len(binary_message):
                    break
            if data_index >= len(binary_message):
                break

        encoded_image_path = os.path.join(os.path.dirname(image_path), "encoded_image.png")
        img.save(encoded_image_path)
        return encoded_image_path
    except Exception as e:
        raise Exception(f"Error during encoding: {e}")

def decode_image(encoded_image_path):
    try:
        img = Image.open(encoded_image_path)
        width, height = img.size
        binary_message = ""

        for row in range(height):
            for col in range(width):
                pixel = img.getpixel((col, row))
                for color_channel in range(3):
                    binary_message += format(pixel[color_channel], '08b')[-1]

        message = ""
        for i in range(0, len(binary_message), 8):
            char = chr(int(binary_message[i:i+8], 2))
            if char == '\0':
                break
            message += char
        return message
    except Exception as e:
        raise Exception(f"Error during decoding: {e}")

def select_image_for_encoding():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_image_path.delete(0, tk.END)
        entry_image_path.insert(0, file_path)

def encode_message():
    image_path = entry_image_path.get()
    message = entry_message.get()
    if not image_path or not message:
        messagebox.showwarning("Warning", "Please select an image and enter a message!")
        return
    try:
        encoded_image_path = encode_image(image_path, message)
        messagebox.showinfo("Success", f"Message encoded successfully! Encoded image saved at: {encoded_image_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_image_for_decoding():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_encoded_image_path.delete(0, tk.END)
        entry_encoded_image_path.insert(0, file_path)

def decode_message():
    encoded_image_path = entry_encoded_image_path.get()
    if not encoded_image_path:
        messagebox.showwarning("Warning", "Please select an encoded image!")
        return
    try:
        message = decode_image(encoded_image_path)
        entry_decoded_message.delete(0, tk.END)
        entry_decoded_message.insert(0, message)
        messagebox.showinfo("Success", "Message decoded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("Image Steganography")

# Encoding section
tk.Label(root, text="Image for Encoding:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_image_path = tk.Entry(root, width=50)
entry_image_path.grid(row=0, column=1, padx=10, pady=5)
btn_browse_image = tk.Button(root, text="Browse", command=select_image_for_encoding)
btn_browse_image.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Message to Encode:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_message = tk.Entry(root, width=50)
entry_message.grid(row=1, column=1, padx=10, pady=5)

btn_encode = tk.Button(root, text="Encode", command=encode_message)
btn_encode.grid(row=2, column=0, columnspan=3, pady=10)

# Decoding section
tk.Label(root, text="Encoded Image:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_encoded_image_path = tk.Entry(root, width=50)
entry_encoded_image_path.grid(row=3, column=1, padx=10, pady=5)
btn_browse_encoded_image = tk.Button(root, text="Browse", command=select_image_for_decoding)
btn_browse_encoded_image.grid(row=3, column=2, padx=10, pady=5)

tk.Label(root, text="Decoded Message:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_decoded_message = tk.Entry(root, width=50)
entry_decoded_message.grid(row=4, column=1, padx=10, pady=5)

btn_decode = tk.Button(root, text="Decode", command=decode_message)
btn_decode.grid(row=5, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
