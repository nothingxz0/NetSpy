import requests
import os
import re
import logging
from colorama import Fore, init
import sys, random, time

yl = Fore.YELLOW
red = Fore.RED
gr = Fore.GREEN

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_folder, 'Reverse_DNS.log'),
    level=logging.DEBUG,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def center_text(text, width):
    return text.center(width)

def logo():
    os.system('cls')
    clear = '\x1b[0m'
    colors = [36]
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

def reverse(ip):
    try:
        response = requests.get(f"https://rapiddns.io/sameip/{ip}?full=1#result", headers=ua).content.decode("utf-8")
        pattern = r"</th>\n<td>(.*?)</td>"
        results = re.findall(pattern, response)
        return results
    except:
        return []

def save_to_file(filename, data):
    with open(filename, "a+") as file:
        for item in data:
            file.write(item + '\n')

def reverse_dns_main():
    
    logo()
    print("<----------------------------------------------------->\n")
    print("This is a reverse DNS tool made coded by NOTHING\n")
    print("<----------------------------------------------------->\n")  
      
    sites = input("Enter the file path containing IP addresses: ")
    output_filename = "reversed_results.txt"
    
    try:
        with open(sites, 'r') as file:
            ip_addresses = file.readlines()
    except FileNotFoundError:
        logging.error("File not found.")
        print("File not found.")
        exit(1)
    
    for ip in ip_addresses:
        ip = ip.strip()
        logging.info(f"Processing IP: {ip}")
        print(f"IP: {ip}")
        
        subdomains_rapiddns = reverse(ip)
        
        if subdomains_rapiddns:
            logging.info("Subdomains found:")
            print("Subdomains from RapidDNS.io:")
            total_subdomains = len(subdomains_rapiddns)
            logging.info(f"Total subdomains found: {total_subdomains}")
            print(f"Total subdomains found: {total_subdomains}")
            save_to_file(output_filename, subdomains_rapiddns)
            logging.info(f"Results appended to '{output_filename}'")
            print(f"Results appended to '{output_filename}'\n")
            
        else:
            logging.info("No subdomains found.")
            print("No subdomains found.\n")
