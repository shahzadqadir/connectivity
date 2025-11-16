# ~/automation/connectivity/configure_fortigate_fw_addresses.py

import paramiko
from connectivity import Connectivity

def configure_fortigate_fw_address(firewall: str, username: str, password: str,                                
                                address_name: str, subnet: str, mask: str):
    configurations = [
        "config firewall address",
        f"edit {address_name}",
        f'set subnet {subnet}/{mask}',
        "end"
    ]

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands(f"show firewall address {address_name}")
    return output

def configure_fortigate_fw_address_group(firewall: str, username: str, password: str,
                                         address_group_name: str, members: list):
    configurations = [
        "config firewall addrgrp",
        f"edit {address_group_name}",
        f"set member {members[0]}"
    ]
    for member in members[1:]:
        configurations.append(f"append member {member}")
    configurations.append("end")

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

    # Check configurations
    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands(f"show firewall addrgrp {address_group_name}")
    return output


if __name__ == "__main__":
    output = configure_fortigate_fw_address("10.10.99.1", 
                                               username="script",
                                               password="cisco123",
                                               address_name="172.16.11.0/24",
                                               subnet="172.16.11.0",
                                               mask="24")
    for line in output:
        print(line)
    
    output = configure_fortigate_fw_address("10.10.99.1", 
                                               username="script",
                                               password="cisco123",
                                               address_name="172.16.12.0/24",
                                               subnet="172.16.12.0",
                                               mask="24")
    for line in output:
        print(line)

    output = configure_fortigate_fw_address("10.10.99.1", 
                                               username="script",
                                               password="cisco123",
                                               address_name="172.16.13.0/24",
                                               subnet="172.16.13.0",
                                               mask="24")
    for line in output:
        print(line)

    output = configure_fortigate_fw_address_group(
        "10.10.99.1",
        username="script",
        password="cisco123",
        address_group_name="SITE1_ADDRESSES",
        members=["172.16.11.0/24", "172.16.12.0/24", "172.16.13.0/24"]
    )
    print(output)

    output = configure_fortigate_fw_address_group(
        "10.10.99.1",
        username="script",
        password="cisco123",
        address_group_name="ALLOW-ANY",
        members=["all"]
    )
    print(output)