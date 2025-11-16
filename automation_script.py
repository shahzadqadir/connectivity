# ~/automation/connectivity/automation_script.py

import paramiko
from connectivity import Connectivity


def create_vlans(switches_list: list, vlans_list: list, 
                 username: str, password: str) -> bool:
    """Takes a list of switches IP address, and a list of vlans
    each element of list of vlans is a tuple that has two elements
    vlan id, and vlan name. Function returns True if there are no errors.
    """
    print("Staring configurations ...")
    for switch in switches_list:
        connection = Connectivity(switch)
           
        for vlan in vlans_list:
            connection.login(username=username, password=password)
            connection.config_cmd_ssh(
                ["configure terminal", f"vlan {vlan[0]}", f"name {vlan[1]}", "exit"]
            )
        print(f"Switch {switch} configured")       
    return True

def show_vlans(switches_list: list, username: str, password: str):
    """Loop over list of switches and run show vlan command"""    
    for switch in switches_list:
        connection = Connectivity(switch)
        connection.login(username=username, password=password)
        output = connection.execute_show_commands("show vlan")
        print(f"Switch: {switch}")
        for line in output:
            print(line)

def configure_trunk(switch: str, username: str, password: str, 
                    port: str, vlans: list):
    """ Configure port as trunk.
    Allows vlans provided in the list of strings"""
    allowed_vlans = ','.join(vlans)    
    connection = Connectivity(switch)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(
        ["configure terminal", 
         f"interface {port}",
         "switchport trunk encapsulation dot1q",
         "switchport mode trunk",
         f"switchport trunk allowed vlan {allowed_vlans}",
         "end"]
        )
    # config_cmd_ssh closes connection so we need to open it again
    connection = Connectivity(switch)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show int trunk")
    return output


def create_svis(router: str, username: str, password: str, svi_info: list):
    """
    svi_info: should be in the format
    [('Ethernet0', '11', '192.168.10.1', '255.255.255.0'),
     ('Ethernet0', '12', '192.168.20.1', '255.255.255.0')]
    
    It must be a list of tuples, each tuple will have interface, vlan, ip_address, 
    and subnet_mask. 
    """
    configurations = ["configure terminal"]
    for line in svi_info:
        configurations.append(f"interface {line[0]}.{line[1]}")
        configurations.append(f"encap dot1q {line[1]}")
        configurations.append(f"ip address {line[2]} {line[3]}")
        configurations.append(f"no shut")
    configurations.append("end")

    connection = Connectivity(router)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)
     # config_cmd_ssh closes connection so we need to open it again
    connection = Connectivity(router)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show ip interface brief")
    return output


def configure_hsrp(router: str, username: str, password: str, svi_info: list):
    """ 
    svi_info format:
    [('sub-interface', 'virtual-ip', 'priority')]
    """
    configurations = ["configure terminal"]
    for line in svi_info:
        configurations.append(f"interface {line[0]}")
        configurations.append(f"standby 1 ip {line[1]}")
        configurations.append(f"standby 1 priority {line[2]}")
        configurations.append(f"standby 1 preempt")
    configurations.append("end")

    connection = Connectivity(router)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

     # config_cmd_ssh closes connection so we need to open it again
    connection = Connectivity(router)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show standby brief")
    return output

# NEW
def configure_bgp(router: str, username: str, password: str, 
                  local_as: str, networks_info: list ):
    """
    networks_info format:
    [('network', 'subnet-mask')]
    """
    configurations = ["configure terminal", f"router bgp {local_as}"]
    for line in networks_info:
        configurations.append(f"network {line[0]} mask {line[1]}")
    configurations.append("end")

    connection = Connectivity(router)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

     # config_cmd_ssh closes connection so we need to open it again
    connection = Connectivity(router)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show bgp ipv4 unicast")
    return output


if __name__ == "__main__":
    
    csr_routers = ["10.10.99.11", "10.10.99.12"]

    for router in csr_routers:
        output = configure_bgp(router=router, username="script", password="cisco123", local_as='65534',
                         networks_info=[
                             ('172.16.11.0', '255.255.255.0'),
                             ('172.16.12.0', '255.255.255.0'),
                             ('172.16.13.0', '255.255.255.0'),
                             ])
        print(f"BGP Table for {router}:")
        for line in output:
            print(line)