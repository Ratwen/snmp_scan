from flask import Flask, send_file, send_from_directory
import os
from scanner.arp_scanner import arp_scan
from scanner.nmap_scanner import nmap_scan
from topology.builder import build_topology
from report.pdf_report import generate_pdf
from report.csv_report import generate_csv
from visualizer.map_generator import generate_html

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('static', 'network_map.html')

@app.route('/download/pdf')
def download_pdf():
    return send_file('network_report.pdf', as_attachment=True)

@app.route('/download/csv')
def download_csv():
    return send_file('network_report.csv', as_attachment=True)

@app.route('/download/pcap')
def download_pcap():
    latest = sorted([f for f in os.listdir('static') if f.endswith('.pcap')])[-1]
    return send_file(f'static/{latest}', as_attachment=True)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    print("[INIT] Сканирование сети...")
    devices = arp_scan()
    devices += nmap_scan(devices)
    from report.pcap_report import capture_network_pcap
    if devices:
        generate_csv(devices)
        generate_pdf(devices)
        graph = build_topology(devices)
        generate_html(graph, devices)
        ip_list = [d['ip'] for d in devices]
        capture_network_pcap(ip_list)
    else:
        with open('static/network_map.html', 'w') as f:
            f.write('<h2>Устройства в сети не найдены.</h2>')

    print("[FLASK] Запускаем сервер Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)