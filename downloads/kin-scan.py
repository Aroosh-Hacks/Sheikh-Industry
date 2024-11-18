import socket
import subprocess
import requests
from scapy.all import ARP, Ether, srp

# Function 1: Network Scanning
def network_scan(ip_range):
    print(f"Scanning network: {ip_range}...")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for _, received in result:
        devices.append({'IP': received.psrc, 'MAC': received.hwsrc})
    
    print("Active Devices:")
    for device in devices:
        print(f"IP: {device['IP']} | MAC: {device['MAC']}")
    return devices

# Function 2: Port Scanning & Service Detection
def port_scan(ip, ports):
    print(f"\nScanning ports on {ip}...")
    open_ports = []
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "Unknown Service"
            open_ports.append({'port': port, 'service': banner})
            print(f"Port {port} is open | Service: {banner}")
        sock.close()
    return open_ports

# Function 3: Vulnerability Scanning using Exploit DB API
def vulnerability_scan(open_ports):
    print("\nChecking for vulnerabilities...")
    exploit_db_url = "https://vuln-api.com/api/v1/search"
    headers = {'User-Agent': 'VulnScanner/1.0'}
    
    for port_info in open_ports:
        service = port_info['service']
        if service != "Unknown Service":
            params = {'query': service}
            try:
                response = requests.get(exploit_db_url, headers=headers, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data['total'] > 0:
                        print(f"Vulnerabilities found for {service}:")
                        for vuln in data['vulnerabilities']:
                            print(f"- {vuln['title']} (CVE: {vuln['cve']})")
                    else:
                        print(f"No known vulnerabilities for {service}.")
                else:
                    print(f"Error accessing vulnerability database.")
            except requests.RequestException as e:
                print(f"Failed to connect: {e}")

# Main Function
if __name__ == "__main__":
    print("Custom Nmap Tool")
    print("1. Network Scan")
    print("2. Port Scan & Service Detection")
    print("3. Vulnerability Scan")
    
    choice = input("Choose an option (1-3): ")
    
    if choice == '1':
        ip_range = input("Enter IP range (e.g., 192.168.1.0/24): ")
        network_scan(ip_range)
    
    elif choice == '2':
        target_ip = input("Enter target IP: ")
        ports = list(map(int, input("Enter ports to scan (comma-separated): ").split(',')))
        open_ports = port_scan(target_ip, ports)
    
    elif choice == '3':
        target_ip = input("Enter target IP: ")
        ports = list(map(int, input("Enter ports to scan (comma-separated): ").split(',')))
        open_ports = port_scan(target_ip, ports)
        if open_ports:
            vulnerability_scan(open_ports)
        else:
            print("No open ports detected.")
    
    else:
        print("Invalid choice. Exiting.")
