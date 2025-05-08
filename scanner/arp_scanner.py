from scapy.layers.l2 import ARP, Ether, srp
import socket
import psutil
import ipaddress
from scanner.snmp import get_device_info

def get_active_subnet():
    for interface, addrs in psutil.net_if_addrs().items():
        print(addrs)
        for addr in addrs:
            if addr.family.name == 'AF_INET' and addr.address.startswith('192.'):
                try:
                    network = ipaddress.IPv4Network(
                        f"{addr.address}/{addr.netmask}",
                        strict=False
                    )
                    print(f"[INFO] Активная подсеть: {network}")
                    return str(network)
                except Exception as e:
                    print(f"[ERROR] Ошибка определения подсети: {e}")
    return "192.168.0.0/24"  # запасной вариант

def arp_scan():
    subnet = get_active_subnet()
    device_list = []

    print(f"[ARP] Сканирование подсети: {subnet}")
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    try:
        answered = srp(packet, timeout=3, verbose=False)[0]
        print(answered)

        for send, recv in answered:
            ip = recv.psrc
            mac = recv.hwsrc
            hostname = socket.getfqdn(ip)
            print(f"[ARP] Найдено устройство: {ip} ({mac})")

            snmp_info = get_device_info(ip)
            device_type = "unknown"

            if ip == "192.168.0.1":
                device_type = "router"
            elif snmp_info:
                snmp_lower = snmp_info.lower()
                if 'tp-link' in snmp_lower or 'router' in snmp_lower or 'gateway' in snmp_lower:
                    device_type = "router"
                elif 'printer' in snmp_lower:
                    device_type = "printer"

            device_list.append({
                "ip": ip,
                "mac": mac,
                "hostname": hostname,
                "type": device_type
            })

    except Exception as e:
        print(f"[ARP] Ошибка сканирования: {e}")

    return device_list