import os
import struct
import socket

# Define the tunnel endpoints
tunnel_src_ip = "10.0.0.32" #ParrotVPN2
tunnel_dest_ip = "10.0.0.31" #ParrotVPN1

# Define the encryption key
key = b"s3cr3tk3y"

# Create a raw socket for the tunnel
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

while True:
    # Receive a packet from the tunnel
    data, addr = sock.recvfrom(65536)

    # Extract the ICMP header and payload from the packet
    icmp_header = data[20:28]
    icmp_payload = data[28:]

    # Check if the packet is an ICMP echo request
    if icmp_header[0] == 8:
        # Decrypt the payload
        decrypted_payload = bytes([a ^ b for a, b in zip(icmp_payload, key)])

        # Extract the destination IP from the decrypted payload
        dest_ip = extract_ip(decrypted_payload)

        # Create a new ICMP echo request with the decrypted payload
        icmp_type = 8
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = os.getpid() & 0xFFFF
        icmp_seq = 1
        icmp_header = struct.pack("bbHHh", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        icmp_packet = icmp_header + decrypted_payload

        # Send the ICMP echo request to the destination
        dest_addr = (dest_ip, 0)
        sock.sendto(icmp_packet, dest_addr)
