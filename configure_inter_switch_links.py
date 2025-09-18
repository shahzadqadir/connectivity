import paramiko
from connectivity import Connectivity

def configure_trunk(switch: str, username: str, password: str,  
                    port: str, vlans: list) -> list:
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

if __name__ == "__main__":        
    switch = "10.10.99.13"
    output = configure_trunk(switch=switch, 
                             username="script", 
                             password="cisco123",
                             port="Ethernet0/0",
                             vlans=['11', '12', '13'])
    print(f"{switch} RESULTS")
    for line in output:
        print(line)
    
    switch = "10.10.99.14"
    output = configure_trunk(switch=switch,
                             username="script",
                             password="cisco123",
                             port="Ethernet0/0",
                             vlans=['11', '12', '13'])
    print("#################")
    print(f"{switch} Results")
    for line in output:
        print(line)
