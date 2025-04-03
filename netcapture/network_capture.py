import subprocess
from scapy.all import *


# Lấy danh sách các giao diện mạng trên hệ thống Windows
def get_interfaces():
    result = subprocess.run(
        ["netsh", "interface", "show", "interface"], capture_output=True, text=True
    )
    output_lines = result.stdout.splitlines()[3:]
    interfaces = [line.split()[3] for line in output_lines if len(line.split()) >= 4]
    return interfaces


# Xử lý gói tin bắt được
def packet_handler(packet):
    if packet.haslayer(Raw):
        print("Captured Packet:")
        print(str(packet))


# In danh sách giao diện mạng cho người dùng
interfaces = get_interfaces()
# Print a list of network interfaces for the user to choose from
print("Danh sách các giao diện mạng:")
for i, iface in enumerate(interfaces, start=1):
    print(f"{i}. {iface}")
# User select network interface
choice = int(input("Chọn một giao diện mạng (nhập số): "))
selected_iface = interfaces[choice - 1]
# Capture packets on selected network interface
sniff(iface=selected_iface, prn=packet_handler, filter="tcp")
