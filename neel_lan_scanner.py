import subprocess
import requests
import re

def scan_network():
    ip_range = '192.168.1.1-255'
    command = ['sudo', 'nmap', '-sn', ip_range]
    result = subprocess.run(command, capture_output=True, text=True)
    output_lines = result.stdout.splitlines()

    devices = []

    for line in output_lines:
        if 'Nmap scan report for' in line:
            device = {}
            # Extract the hostname from the line
            device['Hostname'] = line.split(' ')[-1]
        elif 'MAC Address: ' in line:
            # Extract the MAC address using regex
            mac_match = re.search(r'MAC Address: (.+)', line)
            if mac_match:
                mac_address = mac_match.group(1)

                # Fetch manufacturer based on MAC address
                manufacturer = get_device_manufacturer(mac_address)
                device['MAC Address'] = mac_address
                device['Manufacturer'] = manufacturer

                # Add the device to the list
                devices.append(device)

    # Print the device information in a table-like format
    print("Index  | Hostname                | MAC Address        | Manufacturer")
    print("-" * 66)
    for index, device in enumerate(devices, start=1):
        print(f"{index:6} | {device['Hostname'][:23]:23} | {device['MAC Address']:17} | {device['Manufacturer']}")

def get_device_manufacturer(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    response = requests.get(url)
    if response.status_code == 200:
        manufacturer = response.text
        return manufacturer
    return "Unknown"

scan_network()
