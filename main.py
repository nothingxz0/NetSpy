from NothingDNS import reverse_dns_main
from Ping_Monitoring import main_ping
from Device_Scanner import nmap_scan_main
import sys
import time
import random
import os


def logo():
    os.system('cls')
    clear = '\x1b[0m'
    colors = [95]
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


def clear_terminal():
    
    if os.name == 'nt':
        os.system('cls')

def main():
    

    
    print("\nHello! This is a simple automation tool to Scan, monitor, and manage your network devices.\n")
    print("<---------------------------------------------------------------------------------------------------------->\n")
    print("\033[1;31mNetwork Scanner is under development, we will realize it as soon as possible\033[0m\n")
    print("<---------------------------------------------------------------------------------------------------------->\n")
        
    while True:

        logo()

        print("\nHello! This is a simple automation tool to Scan, monitor, and manage your network devices.\n")
        print("<---------------------------------------------------------------------------------------------------------->\n")
        print("\033[1;31mNetwork Scanner is under development, we will realize it as soon as possible\033[0m\n")
        print("<---------------------------------------------------------------------------------------------------------->\n")
        user_choice = int(input("""1. Device Scanner
2. Ping Monitor2
3. NothingDNS (This is a stand alone programme that perform a reverse IP lookup to discover subdomains associated with a given IP address.)\n
Enter Your Choice (0 to exit): """))
        
        if user_choice == 0:
            clear_terminal()
            sys.exit("Exiting the program...")
           
        elif user_choice == 1:
            nmap_scan_main()
        
        elif user_choice == 2:
            main_ping()
        
        elif user_choice == 3:
            reverse_dns_main()

if __name__ == "__main__":
    main()
    print("testing issues")