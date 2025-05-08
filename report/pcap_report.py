from scapy.all import sr1, wrpcap
from scapy.layers.inet import IP, ICMP
import time

def capture_network_pcap(ip_list, output_file=None):
    packets = []

    for ip in ip_list:
        print(f"[PCAP] Пинг {ip}...")
        pkt = IP(dst=ip) / ICMP()
        ans = sr1(pkt, timeout=1, verbose=0)
        if ans:
            packets.append(ans)

    if not output_file:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"static/capture_{timestamp}.pcap"

    wrpcap(output_file, packets)
    print(f"[PCAP] Сохранено в {output_file}")
    return output_file