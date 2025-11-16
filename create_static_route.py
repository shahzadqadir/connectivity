# ~/automation/connectivity/create_static_route.py

import paramiko
from connectivity import Connectivity

def create_static_route(switch: str, username: str, password: str,
                        destination_subnet: str, destination_mask: str,
                        next_hop_ip: str):
    configurations = [
        "configure terminal",
        f"ip route {destination_subnet} {destination_mask} {next_hop_ip}"
    ]    
    connection = Connectivity(switch)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

    connection = Connectivity(switch)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show ip route")
    return output

if __name__ == "__main__":
    output = create_static_route("10.10.99.2", "script", "cisco123",
                                 "0.0.0.0", "0.0.0.0", "172.16.21.1")
    for line in output:
        print(line)