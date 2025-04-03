import tkinter as tk
from tkinter import ttk, messagebox
from scapy.all import ARP, Ether, srp
import requests


def get_vendor_by_mac(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"


def local_network_scan(ip_range):
    try:
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=3, verbose=0)[0]
        devices = []
        for sent, received in result:
            devices.append(
                {
                    "ip": received.psrc,
                    "mac": received.hwsrc,
                    "vendor": get_vendor_by_mac(received.hwsrc),
                }
            )
        return devices
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []


def scan_network():
    ip_range = ip_entry.get()
    if not ip_range:
        messagebox.showwarning("Input Error", "Please enter an IP range.")
        return

    devices = local_network_scan(ip_range)
    for row in tree.get_children():
        tree.delete(row)

    if devices:
        for device in devices:
            tree.insert(
                "", "end", values=(device["ip"], device["mac"], device["vendor"])
            )
    else:
        messagebox.showinfo("Scan Complete", "No devices found.")


# Create the main window
root = tk.Tk()
root.title("Network Scanner")

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="IP Range:").grid(row=0, column=0, padx=5)
ip_entry = tk.Entry(input_frame, width=30)
ip_entry.grid(row=0, column=1, padx=5)
scan_button = tk.Button(input_frame, text="Scan", command=scan_network)
scan_button.grid(row=0, column=2, padx=5)

# Results frame
results_frame = tk.Frame(root)
results_frame.pack(pady=10)

# Add scrollbar
scrollbar = ttk.Scrollbar(results_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(
    results_frame,
    columns=("IP", "MAC", "Vendor"),
    show="headings",
    yscrollcommand=scrollbar.set,
)
tree.heading("IP", text="IP Address")
tree.heading("MAC", text="MAC Address")
tree.heading("Vendor", text="Vendor")
tree.column("IP", width=150)
tree.column("MAC", width=200)
tree.column("Vendor", width=200)
tree.pack(side="left", fill="both", expand=True)

scrollbar.config(command=tree.yview)

# Run the application
root.mainloop()
