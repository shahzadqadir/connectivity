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

def configure_fortigate_port(firewall: str, username: str, password: str, 
                             port: str, ip: str, mask: str, mgmt_access: list,
                             alias: str, role: str, status: str):
    configurations = [
        "conf system interface",
        f"edit {port}",
        "set mode static",
        f"set ip {ip} {mask}",
        f'set alias "{alias}"',
        f"set status {status}",
        f"set role {role}"
    ]
    allowed_mgmt_access = "set allowaccess "
    for item in mgmt_access:
        allowed_mgmt_access += item + " "
    configurations.append(allowed_mgmt_access)
    configurations.append("end")

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands(f"show system interface {port}")
    return output

def configure_fortigate_fw_policy(firewall: str, username: str, password: str,
                                policy_name: str, src_int: str, dest_int: str,
                                action: str="accept", src_address: str="all", 
                                dest_address: str="all", schedule: str="always", 
                                service: str="ALL", logg_traffic: str="all"):
    configurations = [
        "config firewall policy",
        "edit 1",
        f'set name "{policy_name}"',
        f'set srcintf "{src_int}"',
        f'set dstintf "{dest_int}"',
        f'set action {action}',
        f'set srcaddr "{src_address}"',
        f'set dstaddr "{dest_address}"',
        f'set schedule "{schedule}"',
        f'set service "{service}"',
        f'set logtraffic all',
        "end"
    ]

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show firewall policy")
    return output

def configure_vlan_and_svi(switch: str, username: str, password: str, vlan: str,
                           ports: str, create_svi: bool=False, svi_ip: str="",
                           svi_mask: str=""):
    """ This function configures a VLAN on the provided list of ports,
    If create_svi parameter is True then It also configures an SVI for the VLAN.
    """
    configurations = [
        "configure terminal"
    ]
    for port in ports:
        configurations.append(f"interface {port}")
        configurations.append("switchport mode access")
        configurations.append(f"switchport access vlan {vlan}")
        configurations.append("no shutdown")
    if create_svi:
        configurations.append(f"interface vlan{vlan}")
        configurations.append(f"ip address {svi_ip} {svi_mask}")
        configurations.append("no shutdown")

    connection = Connectivity(switch)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

    connection = Connectivity(switch)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show ip interface brief")
    return output

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
       
def test_connectivity(source_device: str, username: str, password: str,
                      source_ip: str, destination_ip: str):
    connection = Connectivity(source_device)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands(f"ping {destination_ip} source {source_ip}")
    return output
        
        

if __name__ == "__main__":
    # switches = ["10.10.99.13", "10.10.99.14"]
    # create_vlans(switches_list=switches,
    #              vlans_list=[(11, "Prod"), (12, "Dev"), (13, "Dev-Test")],
    #              username='script', password='cisco123')
    # show_vlans(switches_list=switches, 
    #            username='script', password='cisco123')
    # switch = "10.10.99.13"
    # output = configure_trunk(switch=switch, username="script", password="cisco123", 
    #                 port="Ethernet0/0", vlans=['11', '12', '13'])
    # print(f"{switch} RESULTS")
    # for line in output:
    # NEW
    # for line in output:
    #     print(line)

    # switch = "10.10.99.13"
    # output = configure_trunk(switch=switch, username="script", password="cisco123", 
    #                 port="Ethernet0/1", vlans=['11', '12', '13'])
    # print(f"{switch} Results - SW1 to CSR1")
    # for line in output:
    #     print(line)
    
    # switch = "10.10.99.14"
    # output = configure_trunk(switch=switch, username="script", password="cisco123", 
    #                 port="Ethernet0/1", vlans=['11', '12', '13'])
    # print("#################")
    # print(f"{switch} Results - SW2 to CSR2")
    # for line in output:
    #     print(line)

    # router = "10.10.99.11"
    # output = create_svis(router=router, username="script", password="cisco123", 
    #                      svi_info=[
    #                          ('GigabitEthernet2', '11', '172.16.11.1', '255.255.255.0'),
    #                          ('GigabitEthernet2', '12', '172.16.12.1', '255.255.255.0'),
    #                          ('GigabitEthernet2', '13', '172.16.13.1', '255.255.255.0'),
    #                          ])
    # for line in output:
    #     print(line)
    
    # router = "10.10.99.12"
    # output = create_svis(router=router, username="script", password="cisco123", 
    #                      svi_info=[
    #                          ('GigabitEthernet2', '11', '172.16.11.2', '255.255.255.0'),
    #                          ('GigabitEthernet2', '12', '172.16.12.2', '255.255.255.0'),
    #                          ('GigabitEthernet2', '13', '172.16.13.2', '255.255.255.0'),
    #                          ])
    # for line in output:
    #     print(line)


    # router = "10.10.99.11"
    # output = configure_hsrp(router=router, username="script", password="cisco123", 
    #                      svi_info=[
    #                          ('GigabitEthernet2.11', '172.16.11.254', '130'),
    #                          ('GigabitEthernet2.12', '172.16.12.254', '130'),
    #                          ('GigabitEthernet2.13', '172.16.13.254', '130'),
    #                          ])
    # for line in output:
    #     print(line)


    # router = "10.10.99.12"
    # output = configure_hsrp(router=router, username="script", password="cisco123", 
    #                      svi_info=[
    #                          ('GigabitEthernet2.11', '172.16.11.254', '120'),
    #                          ('GigabitEthernet2.12', '172.16.12.254', '120'),
    #                          ('GigabitEthernet2.13', '172.16.13.254', '120'),
    #                          ])
    # for line in output:
    #     print(line)

    # csr_routers = ["10.10.99.11", "10.10.99.12"]

    # for router in csr_routers:
    #     output = configure_bgp(router=router, username="script", password="cisco123", local_as='65534',
    #                      networks_info=[
    #                          ('172.16.11.0', '255.255.255.0'),
    #                          ('172.16.12.0', '255.255.255.0'),
    #                          ('172.16.13.0', '255.255.255.0'),
    #                          ])
    #     print(f"BGP Table for {router}:")
    #     for line in output:
    #         print(line)

    # output = configure_fortigate_port(firewall="10.10.99.1", username="admin", password="cisco123", 
    #                          port="port2", ip="172.16.21.1", mask="255.255.255.0", 
    #                          mgmt_access=["ssh", "ping"], alias="inside", 
    #                          role="lan", status="up")
    # for line in output:
    #     print(line)

    # output = configure_fortigate_fw_policy("10.10.99.1", username="admin", password="cisco123",
    #                                        policy_name="inside-outside", src_int="port2",
    #                                        dest_int="port1", action="accept", 
    #                                        src_address="all", dest_address="all")
    # for line in output:
    #     print(line)

    # output = configure_vlan_and_svi("10.10.99.2", "script", "cisco123", "10",
    #                                 ["Ethernet0/0", "Ethernet0/2"], True, "172.16.21.2", "255.255.255.0")
    # for line in output:
    #     print(line)

    # output = create_static_route("10.10.99.2", "script", "cisco123",
    #                              "0.0.0.0", "0.0.0.0", "172.16.21.1")
    # for line in output:
    #     print(line)

    output = test_connectivity("10.10.99.2", "script", "cisco123",
                               "172.16.21.2", "172.16.11.1")
    for line in output:
        print(line)

