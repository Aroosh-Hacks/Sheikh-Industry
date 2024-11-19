from scapy.all import sniff, IP, TCP, UDP
import threading
import time

# List to store captured packets
captured_packets = []

# Flag to control continuous packet capturing
capturing = True

# File to save captured packets
output_file = "captured_packets.txt"

# Function to display packet details and store them in a file
def packet_callback(packet):
    if not capturing:
        return  # Stop capturing if paused

    packet_details = {}
    
    if packet.haslayer(IP):  # Check if the packet has an IP layer
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        packet_details['IP'] = (ip_src, ip_dst)
        
        if packet.haslayer(TCP):  # If the packet has a TCP layer
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            packet_details['TCP'] = (tcp_sport, tcp_dport)
        
        elif packet.haslayer(UDP):  # If the packet has a UDP layer
            udp_sport = packet[UDP].sport
            udp_dport = packet[UDP].dport
            packet_details['UDP'] = (udp_sport, udp_dport)
        
        # Save packet details to the list and file
        captured_packets.append(packet_details)
        with open(output_file, "a") as f:
            f.write(f"{packet_details}\n")
        
        # Print the packet details
        print(f"Captured Packet: {packet_details}")

# Function to access captured packets
def access_captured_packets():
    print("\nAccessing Captured Packets:")
    for index, packet in enumerate(captured_packets, start=1):
        print(f"Packet {index}: {packet}")

# Function to start capturing packets
def start_sniffing():
    print("Starting continuous packet sniffing... Press 'p' to pause, 'r' to resume, 'q' to quit.")
    sniff(prn=packet_callback, store=0)

# Function to pause capturing
def pause_capture():
    global capturing
    capturing = False
    print("Capture paused. Press 'r' to resume.")

# Function to resume capturing
def resume_capture():
    global capturing
    capturing = True
    print("Capture resumed.")

# Function to listen for user input commands
def listen_for_commands():
    while True:
        command = input("\nEnter command: ")
        
        if command.lower() == 'p':  # Pause the capture
            pause_capture()
        elif command.lower() == 'r':  # Resume the capture
            resume_capture()
        elif command.lower() == 'q':  # Stop the capture and exit
            print("Stopping packet capture.")
            break
        elif command.lower() == 'a':  # Access captured packets
            access_captured_packets()
        else:
            print("Invalid command. Use 'p' to pause, 'r' to resume, 'q' to quit.")

# Run the sniffing in a separate thread to keep it continuous
capture_thread = threading.Thread(target=start_sniffing)
capture_thread.start()

# Listen for commands in the main thread
listen_for_commands()

# Ensure the sniffing thread stops when done
capture_thread.join()
