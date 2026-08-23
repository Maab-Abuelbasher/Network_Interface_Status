# This program will connect to a network device and retrieve the interface status using Netmiko. It will then display the interface status in a readable format.

#import netmiko and os
from netmiko import ConnectHandler  
import os

# import prometheus_client and re
from prometheus_client import start_http_server, Gauge
import re
import time

# --- Metric definition ---
interface_status = Gauge(
    'router_interface_status',
    'Cisco interface status (1=up, 0=down)',
    ['interface', 'status', 'protocol']
)

show_commands = [
    "show ip interface brief",
    #"show version",
    #"show running-config"
]

def check_router_interfaces():
    try:
        connection = ConnectHandler(
            host=os.environ.get("router-ip"),
            username="admin",
            password=os.environ.get("router-password"),
            device_type="cisco_ios"
        )
 
        output = ""
        for cmd in show_commands:
            output += connection.send_command(cmd) + "\n\n"
 
        connection.disconnect()
        print(output)  # kept so you still see it in kubectl logs
 
        parse_interface_output(output)
 
    except Exception as e:
        # IMPORTANT: without this try/except, any SSH failure crashes
        # the whole app and Kubernetes restarts it -> CrashLoopBackOff
        print(f"Error connecting to router: {e}")


def parse_interface_output(output):
    # Matches lines like:
    # GigabitEthernet1   192.168.8.20   YES DHCP   up                    up
    # GigabitEthernet2   unassigned     YES NVRAM  administratively down down
    pattern = re.compile(
        r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(up|down|administratively down)\s+(up|down)',
        re.MULTILINE
    )
 
    for match in pattern.finditer(output):
        iface_name = match.group(1)
        status = match.group(5)
        protocol = match.group(6)
 
        # 1 = fully up (status AND protocol both up), 0 = anything else
        is_up = 1 if (status == "up" and protocol == "up") else 0
 
        interface_status.labels(
            interface=iface_name,
            status=status,
            protocol=protocol
        ).set(is_up)
 

# # Connect to switch using SSH
# connection = ConnectHandler(
#     host=os.environ.get("router-ip"), username="admin", password=os.environ.get("router-password"), device_type="cisco_ios")

# output = ""
# for cmd in show_commands:
#     output += connection.send_command(cmd) + "\n\n"

# print(output)

# connection.disconnect()

if __name__ == '__main__':
    start_http_server(8000)
    print("Metrics server started on :8000/metrics")
    
    while True:
        check_router_interfaces()
        time.sleep(300)  # adjust polling frequency as needed