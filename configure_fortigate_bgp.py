# ~/automation/connectivity/configure_fortigate_bgp.py

import paramiko
from connectivity import Connectivity

def configure_fortigate_bgp(firewall_ip: str, username: str, 
                             password: str) -> bool:
    configurations = [
        "conf router bgp",
        "config redistribute connected",
        "set status enable",
        "end"
    ]
    connection = Connectivity(firewall_ip)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)
    return True

if __name__ == "__main__":
    if configure_fortigate_bgp("10.10.99.1", "admin", "cisco123"):
        print("Connected interfaces advertised successfully!")