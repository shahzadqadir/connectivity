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
    #     print(line)
    
    # switch = "10.10.99.14"
    # output = configure_trunk(switch=switch, username="script", password="cisco123", 
    #                 port="Ethernet0/0", vlans=['11', '12', '13'])
    # print("#################")
    # print(f"{switch} Results")
    # for line in output:
    #     print(line)

    switch = "10.10.99.13"
    output = configure_trunk(switch=switch, username="script", password="cisco123", 
                    port="Ethernet0/1", vlans=['11', '12', '13'])
    print(f"{switch} Results - SW1 to CSR1")
    for line in output:
        print(line)
    
    switch = "10.10.99.14"
    output = configure_trunk(switch=switch, username="script", password="cisco123", 
                    port="Ethernet0/1", vlans=['11', '12', '13'])
    print("#################")
    print(f"{switch} Results - SW2 to CSR2")
    for line in output:
        print(line)

    




