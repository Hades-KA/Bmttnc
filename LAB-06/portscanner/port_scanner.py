from scapy.all import *
# Danh sách cổng phổ biến
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]
# Quét các cổng trong danh sách COMMON_PORTS trên máy chủ được xác định bởi tên miền và kiểm tra xem cổng đó có mở hay không.
def scan_common_ports (target_domain, timeout=2):
    open_ports = []
    target_ip = socket.gethostbyname(target_domain)
    for port in COMMON_PORTS:
        response = sr1(IP(dst=target_ip)/TCP (dport=port, flags="S"),
        timeout=timeout, verbose=0)
        if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
            open_ports.append(port)
            send(IP(dst=target_ip)/TCP(dport=port, flags="R"), verbose=0)
    return open_ports
def main():
    target_domain = input("Enter the target domain: ")
    open_ports = scan_common_ports (target_domain)
    if open_ports:
        print("Open common ports:")
        print(open_ports)
    else:
        print("No open common ports found.")
if __name__ == '__main__':
    main()