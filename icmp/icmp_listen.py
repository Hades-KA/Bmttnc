from scapy.all import *
# Hàm này được gọi mỗi khi có một gói tin đến mà phù hợp với bộ lọc đã định nghĩa (ở đây là gói ICMP).
def packet_callback(packet):
    if packet.haslayer(ICMP):
        icmp_packet = packet[ICMP]  
        print("ICMP Packet Information:")
        print(f"Source IP: {packet[IP].src}")
        print(f"Destination IP: {packet [IP].dst}")
        print(f"Type: {icmp_packet.type}")
        print(f"Code: {icmp_packet.code}")
        print(f"ID: {icmp_packet.id}")
        print(f"Sequence: {icmp_packet.seq}")
        print(f"Load: {icmp_packet.load}")
        print("=" * 30)
# Hàm này dùng để bắt đầu quá trình lắng nghe (sniff) các gói tin trên mạng
def main():
    sniff(prn=packet_callback, filter="icmp", store=0)
if __name__ == '__main__':
    main()