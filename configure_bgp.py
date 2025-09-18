import paramiko
from connectivity import Connectivity

def configure_bgp(router: str, username: str, password: str, 
                  local_as: str, networks_info: list ) -> list:
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
        output = configure_bgp(router=router,
                               username="script",
                               password="cisco123",
                               local_as='65534',
                               networks_info=[
                                   ('172.16.11.0', '255.255.255.0'),
                                   ('172.16.12.0', '255.255.255.0'),
                                   ('172.16.13.0', '255.255.255.0'),
                               ])
        print(f"BGP Table for {router}:")
        for line in output:
            print(line)
