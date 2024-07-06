import subprocess
import schedule
import time
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import sys
import os
import json

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/ping_monitoring.log', level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def configure_email():
    config = load_config()
    print("Email Configuration:")
    config['smtp_server'] = input("SMTP Server: ")
    config['smtp_port'] = int(input("SMTP Port: "))
    config['sender_email'] = input("Sender Email: ")
    config['sender_password'] = input("Sender Password: ")
    config['receiver_email'] = input("Receiver Email: ")
    save_config(config)
    print("Email configuration saved.")

def send_email(subject, body):
    config = load_config()
    if not config:
        print("Email configuration not found. Please configure email first.")
        return

    try:
        smtp_server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        smtp_server.starttls()
        smtp_server.login(config['sender_email'], config['sender_password'])
        
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = config['receiver_email']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        smtp_server.send_message(msg)
        logging.info(f"Email notification sent: {subject}")
        print(f"Email notification sent: {subject}")

        smtp_server.quit()
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}", exc_info=True)

def ping_device(ip_address):
    logging.debug(f"Pinging device: {ip_address}")
    try:
        output = subprocess.check_output(["ping", "-n", "1", ip_address.strip()], timeout=2)
        logging.debug(f"Ping output: {output}")
        return True
    except subprocess.TimeoutExpired:
        logging.warning(f"Ping to {ip_address} timed out.")
        send_email(f"Ping Timeout Alert - {ip_address}", f"Ping to {ip_address} timed out.")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Ping to {ip_address} failed: {e}", exc_info=True)
        send_email(f"Ping Failed Alert - {ip_address}", f"Ping to {ip_address} failed: {e}")
        return False

def monitor_device(ip_address):
    logging.info(f"Monitoring device: {ip_address}")
    if ping_device(ip_address):
        logging.info(f"Device {ip_address} is up!")
        print(f"Device {ip_address} is up!")
    else:
        logging.info(f"Device {ip_address} is down!")
        print(f"Device {ip_address} is down!")

def schedule_ping(ip_addresses, interval):
    logging.info(f"Scheduling ping for {len(ip_addresses)} devices every {interval} seconds")
    for ip_address in ip_addresses:
        logging.info(f"Scheduling ping for {ip_address}")
        schedule.every(interval).seconds.do(monitor_device, ip_address)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logging.error(f"Error in scheduling ping: {e}", exc_info=True)

def logo():
    os.system('cls')
    clear = '\x1b[0m'
    colors = [34]
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

def main_ping():
    logo()
    print("<----------------------------------------------------->\n")
    print("Welcome to the Ping Monitor\n")
    print("<----------------------------------------------------->\n")
    
    logging.info("Program started")
    
    while True:
        option = input("Choose an option:\n1. Ping specific device(s)\n2. Start automatic ping\n3. Configure Email\n4. Exit\nYour choice: ")
        logging.info(f"User selected option {option}")

        if option == "1":
            while True:
                ip_addresses = input("Enter the IP addresses to ping (comma-separated): ").split(',')
                logging.info(f"User entered IP addresses: {ip_addresses}")
                for ip_address in ip_addresses:
                    result = ping_device(ip_address.strip())
                    if result:
                        logging.info(f"Device {ip_address} is up!")
                        print(f"Device {ip_address} is up!")
                    else:
                        logging.info(f"Device {ip_address} is down!")
                        print(f"Device {ip_address} is down!")
                
                choice = input("Do you want to ping another device? (y/n): ")
                if choice.lower() != "y":
                    break
        elif option == "2":
            ip_addresses = input("Enter the IP addresses to ping (comma-separated): ").split(',')
            logging.info(f"User entered IP addresses: {ip_addresses}")
            interval = int(input("Enter the ping interval in seconds: "))
            logging.info(f"User entered ping interval: {interval} seconds")
            schedule_ping(ip_addresses, interval)
        elif option == "3":
            configure_email()
        elif option == "4":
            logging.info("User selected to exit the program")
            print("Exiting the program.")
            break
        else:
            logging.warning("Invalid option selected")
            print("Invalid option. Please choose a valid option.")
            