import nmap
import logging
import random
import sys
import os
import time

def setup_logging():
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, "Device_Scanner.log")
    logging.basicConfig(filename=log_file, level=logging.DEBUG, filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input():
    ip_addr = input("Please enter the IP address you want to scan: ")
    logging.info(f"User entered IP address: {ip_addr}")
    print(f"IP Address: {ip_addr}")

    resp = input("""\nPlease enter the type of scan you want to run
                    1) SYN ACK Scan
                    2) UDP Scan
                    3) Comprehensive Scan \nYour Choice: """)
    logging.info(f"User selected scan type: {resp}")
    print(f"Scan Type: {resp}")

    return ip_addr, resp

def perform_scan(ip_addr, resp):
    scanner = nmap.PortScanner()
    logging.info(f"nmap version: {scanner.nmap_version()}")

    resp_dict = {
        '1': ['-v -sS -O -sV -sC --traceroute', 'tcp'],
        '2': ['-v -sU -O -sV -sC --traceroute', 'udp'],
        '3': ['-v -sS -sV -sC -A -O --traceroute', 'tcp']
    }

    if resp not in resp_dict.keys():
        logging.error("Invalid scan type selected")
        print("Enter a valid option")
        return

    scanner.scan(ip_addr, "1-1024", resp_dict[resp][0])
    logging.info(f"Scan completed for {ip_addr}")

    print("\nScan Results:")
    print("----------------")

    if scanner[ip_addr].state() == 'up':
        logging.info(f"{ip_addr} is up")
        print(f"IP Address: {ip_addr} is up")
        print(f"Protocols: {scanner[ip_addr].all_protocols()}")
        print(f"Open Ports: {scanner[ip_addr][resp_dict[resp][1]].keys()}")

        if 'osmatch' in scanner[ip_addr]:
            os_info = scanner[ip_addr]['osmatch'][0]
            print(f"OS: {os_info['name']} (Accuracy: {os_info['accuracy']})")
        else:
            print("OS information not available")

        if 'ersion' in scanner[ip_addr]:
            version_info = scanner[ip_addr]['version']
            print(f"Version: {version_info}")

        if 'cript' in scanner[ip_addr]:
            script_info = scanner[ip_addr]['script']
            print(f"Script Results: {script_info}")

        if 'traceroute' in scanner[ip_addr]:
            traceroute_info = scanner[ip_addr]['traceroute']
            print(f"Traceroute: {traceroute_info}")

        print("\n")
    else:
        logging.info(f"{ip_addr} is down")
        print(f"IP Address: {ip_addr} is down")

def logo():
    os.system('cls')
    clear = '\x1b[0m'
    colors = [32]
    x = '''
███╗   ██╗███████╗████████╗███████╗██████╗ ██╗   ██╗
████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗╚██╗ ██╔╝
██╔██╗ ██║█████╗     ██║   ███████╗██████╔╝ ╚████╔╝ 
██║╚██╗██║██╔══╝     ██║   ╚════██║██╔═══╝   ╚██╔╝  
██║ ╚████║███████╗   ██║   ███████║██║        ██║   MADE WITH LOVE BY NOTHING <3
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝        ╚═╝   Version 1.0
                                                 
'''
    for N, line in enumerate(x.split('\n')):
        sys.stdout.write('\x1b[1;%dm%s%s\n' % (random.choice(colors), line, clear))
        time.sleep(0.05)

def nmap_scan_main():
    setup_logging()

    logo()

    print("\n<----------------------------------------------------->\n")
    print("Welcome to the Device Scanner\n")
    print("<----------------------------------------------------->\n")

    while True:
        ip_addr, resp = get_user_input()
        perform_scan(ip_addr, resp)

        choice = input("Do you want to scan again? (y/n): ")
        if choice.lower() != 'y':
            break