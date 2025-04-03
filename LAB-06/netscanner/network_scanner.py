import requests
from scapy.all import ARP, Ether, srp


# Quét dải địa chỉ IP được chỉ định để tìm các thiết bị trên mạng
def local_network_scan(ip_range):
    print(f"Scanning the network range: {ip_range}")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Corrected MAC address
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
        )  # Fixed indentation
    return devices


# Lấy thông tin nhà sản xuất (vendor) của thiết bị dựa trên địa chỉ MAC
def get_vendor_by_mac(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except Exception as e:
        print("Error fetching vendor information:", e)
        return "Unknown"


# Điều phối quá trình quét mạng và hiển thị kết quả
def main():
    ip_range = "10.12.132.69/24" # vô CMD và gõ lệnh ipconfig lấy Ipv4
    devices = local_network_scan(ip_range)
    print("Devices on the local network:")
    if not devices:
        print("No devices found.")  # Thêm thông báo khi không tìm thấy thiết bị
    else:
        for device in devices:
            print(
                f"IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}"
            )
    print()


if __name__ == "__main__":
    main()
