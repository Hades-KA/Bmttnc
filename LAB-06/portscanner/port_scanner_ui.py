import tkinter as tk
from tkinter import ttk, messagebox
from scapy.all import IP, TCP, sr1, send
import socket

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]

def scan_common_ports(target_domain, timeout=2):
    try:
        open_ports = []
        target_ip = socket.gethostbyname(target_domain)
        for port in COMMON_PORTS:
            response = sr1(IP(dst=target_ip)/TCP(dport=port, flags="S"), timeout=timeout, verbose=0)
            if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
                open_ports.append(port)
                send(IP(dst=target_ip)/TCP(dport=port, flags="R"), verbose=0)
        return open_ports
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

def start_scan():
    target_domain = domain_entry.get()
    if not target_domain:
        messagebox.showwarning("Input Error", "Please enter a target domain.")
        return

    for row in tree.get_children():
        tree.delete(row)

    open_ports = scan_common_ports(target_domain)
    if open_ports:
        for port in open_ports:
            tree.insert("", "end", values=(port, "Open"))
    else:
        messagebox.showinfo("Scan Complete", "No open common ports found.")

# Create the main window
root = tk.Tk()
root.title("Port Scanner")

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Target Domain:").grid(row=0, column=0, padx=5)
domain_entry = tk.Entry(input_frame, width=30)
domain_entry.grid(row=0, column=1, padx=5)
scan_button = tk.Button(input_frame, text="Scan", command=start_scan)
scan_button.grid(row=0, column=2, padx=5)

# Results frame
results_frame = tk.Frame(root)
results_frame.pack(pady=10)

# Add scrollbar
scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(results_frame, columns=("Port", "Status"), show="headings", yscrollcommand=scrollbar.set)
tree.heading("Port", text="Port")
tree.heading("Status", text="Status")
tree.column("Port", width=100)
tree.column("Status", width=100)
tree.pack(side="left", fill="both", expand=True)

scrollbar.config(command=tree.yview)

# Run the application
root.mainloop()
