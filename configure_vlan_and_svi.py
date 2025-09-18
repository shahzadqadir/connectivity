import paramiko
from connectivity import Connectivity

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

if __name__ == "__main__":
    output = configure_vlan_and_svi(
        switch="10.10.99.2",
        username="script",
        password="cisco123",
        vlan="10",
        ports=["Ethernet0/0", "Ethernet0/2"],
        create_svi=True,
        svi_ip="172.16.21.2",
        svi_mask="255.255.255.0"
    )
    for line in output:
        print(line)
