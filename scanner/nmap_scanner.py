# scanner/nmap_scanner.py
import nmap
import xml.etree.ElementTree as ET
from socket import getfqdn

def nmap_scan(existing_devices):
    """
    Выполняет Nmap-сканирование подсети и возвращает список новых устройств.
    Устройства из existing_devices не дублируются.
    """
    ips_found = [d['ip'] for d in existing_devices]
    target_subnet = _get_subnet(existing_devices)

    print(f"[NMAP] Запуск сканирования подсети: {target_subnet}")
    device_list = []

    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target_subnet, arguments='-F -sV -O')
        xml_data = nm.get_nmap_last_output()

        root = ET.fromstring(xml_data)
        for host in root.findall('host'):
            ip_elem = host.find("address[@addrtype='ipv4']")
            if ip_elem is None:
                continue

            ip = ip_elem.get('addr')
            if ip in ips_found:
                continue

            mac_elem = host.find("address[@addrtype='mac']")
            mac = mac_elem.get('addr') if mac_elem is not None else "unknown"

            hostname_elem = host.find("hostnames/hostname")
            hostname = hostname_elem.get('name') if hostname_elem is not None else getfqdn(ip)

            ports = _extract_open_ports(host)
            device_type = _determine_type_by_ports(host, ports)

            print(f"[NMAP] Найдено: {ip} ({hostname}), тип: {device_type}, порты: {ports}")
            device_list.append({
                "ip": ip,
                "mac": mac,
                "hostname": hostname,
                "type": device_type,
                "ports": ports
            })

    except Exception as e:
        print(f"[NMAP] Ошибка сканирования: {e}")

    return device_list

def _extract_open_ports(host):
    """
    Возвращает список открытых портов и состояний.
    """
    ports = []
    for port in host.findall('ports/port'):
        portid = port.get('portid')
        state_elem = port.find('state')
        service_elem = port.find('service')

        if state_elem is not None and state_elem.get('state') == 'open':
            service_name = service_elem.get('name', '') if service_elem is not None else ''
            ports.append({
                'port': int(portid),
                'service': service_name
            })
    return ports

def _determine_type_by_ports(host, ports):
    """
    Определяет тип устройства по списку портов и сервисов.
    """
    for p in ports:
        portid = str(p['port'])
        service_name = p['service']

        if portid == '631' or 'printer' in service_name:
            return "printer"
        elif portid in ['22', '23', '3389'] or 'ssh' in service_name or 'telnet' in service_name:
            return "router"
        elif portid in ['80', '443'] or 'http' in service_name:
            return "server"
        elif portid == '7547':
            return "cwmp-device"

    return "workstation"

def _get_subnet(devices):
    """
    Попытка получить подсеть из одного из найденных IP-адресов.
    Если ничего не найдено — возвращает 192.168.0.0/24.
    """
    if not devices:
        return "192.168.0.0/24"

    ip = devices[0]["ip"]
    parts = ip.split(".")
    return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"