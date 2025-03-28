import tkinter as tk
from tkinter import messagebox
import base64

def encode_data():
    input_string = entry_input.get()
    if not input_string:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập thông tin cần mã hóa!")
        return
    encoded_bytes = base64.b64encode(input_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    with open("data.txt", "w") as file:
        file.write(encoded_string)
    entry_output.delete(0, tk.END)
    entry_output.insert(0, encoded_string)
    messagebox.showinfo("Thành công", "Đã mã hóa và ghi vào tệp data.txt")

def decode_data():
    try:
        with open("data.txt", "r") as file:
            encoded_string = file.read().strip()
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode("utf-8")
        entry_output.delete(0, tk.END)
        entry_output.insert(0, decoded_string)
        messagebox.showinfo("Thành công", "Đã giải mã chuỗi từ tệp data.txt")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể giải mã: {e}")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Base64 Encoder/Decoder")

# Nhãn và ô nhập thông tin
tk.Label(root, text="Nhập thông tin cần mã hóa:").grid(row=0, column=0, padx=10, pady=10)
entry_input = tk.Entry(root, width=50)
entry_input.grid(row=0, column=1, padx=10, pady=10)

# Nút mã hóa
btn_encode = tk.Button(root, text="Mã hóa", command=encode_data)
btn_encode.grid(row=1, column=0, padx=10, pady=10)

# Nút giải mã
btn_decode = tk.Button(root, text="Giải mã", command=decode_data)
btn_decode.grid(row=1, column=1, padx=10, pady=10)

# Nhãn và ô hiển thị kết quả
tk.Label(root, text="Kết quả:").grid(row=2, column=0, padx=10, pady=10)
entry_output = tk.Entry(root, width=50)
entry_output.grid(row=2, column=1, padx=10, pady=10)

# Chạy vòng lặp giao diện
root.mainloop()
