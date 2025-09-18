import paramiko
from connectivity import Connectivity


def create_svis(router: str, username: str, password: str, svi_info: list) -> list:
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
     # config_cmd_ssh closes connection so we need to open it again to run show commands
    connection = Connectivity(router)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show ip interface brief")
    return output

if __name__ == "__main__":    
    router = "10.10.99.11"
    output = create_svis(router=router, username="script", password="cisco123", 
                         svi_info=[
                             ('GigabitEthernet2', '11', '172.16.11.1', '255.255.255.0'),
                             ('GigabitEthernet2', '12', '172.16.12.1', '255.255.255.0'),
                             ('GigabitEthernet2', '13', '172.16.13.1', '255.255.255.0'),
                             ])
    for line in output:
        print(line)
    
    router = "10.10.99.12"
    output = create_svis(router=router, username="script", password="cisco123", 
                         svi_info=[
                             ('GigabitEthernet2', '11', '172.16.11.2', '255.255.255.0'),
                             ('GigabitEthernet2', '12', '172.16.12.2', '255.255.255.0'),
                             ('GigabitEthernet2', '13', '172.16.13.2', '255.255.255.0'),
                             ])
    for line in output:
        print(line)
