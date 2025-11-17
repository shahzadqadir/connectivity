# This is orcestration script that is used to establish end to end connectivity between sites
# Part of Full Stack Network Automation book by Shahzad Qadir

from automation_script import *
from configure_fortigate_bgp import configure_fortigate_bgp
from configure_fortigate_fw_addresses import (configure_fortigate_fw_address,
                                              configure_fortigate_fw_address_group)
from configure_fortigate_port import configure_fortigate_port
from configure_fortigate_fw_policy import configure_fortigate_fw_policy
from configure_vlan_and_svi import configure_vlan_and_svi
from create_static_route import create_static_route
from test_connectivity import test_connectivity


if __name__ == "__main__":
    # CREATE VLANS
    switches = ["10.10.99.13", "10.10.99.14"]
    create_vlans(switches_list=switches,
                 vlans_list=[(11, "Prod"), (12, "Dev"), (13, "Dev-Test")],
                 username='script', password='cisco123')
    show_vlans(switches_list=switches, 
               username='script', password='cisco123')
    
    # TRUNK BETWEEN SWITCHES
    switch = "10.10.99.13"
    output = configure_trunk(switch=switch, username="script", password="cisco123", 
                    port="Ethernet0/0", vlans=['11', '12', '13'])
    print(f"{switch} RESULTS")
    for line in output:
        print(line)

    switch = "10.10.99.14"
    output = configure_trunk(switch=switch, username="script", password="cisco123", 
                    port="Ethernet0/0", vlans=['11', '12', '13'])
    print("#################")
    print(f"{switch} Results")
    for line in output:
        print(line)

    # TRUNKS TO CSRs
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
    

    # CREATE SVIs
    
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

    # CONFIGURE HSPR

    router = "10.10.99.11"
    output = configure_hsrp(router=router, username="script", password="cisco123", 
                         svi_info=[
                             ('GigabitEthernet2.11', '172.16.11.254', '130'),
                             ('GigabitEthernet2.12', '172.16.12.254', '130'),
                             ('GigabitEthernet2.13', '172.16.13.254', '130'),
                             ])
    for line in output:
        print(line)

    router = "10.10.99.12"
    output = configure_hsrp(router=router, username="script", password="cisco123", 
                         svi_info=[
                             ('GigabitEthernet2.11', '172.16.11.254', '120'),
                             ('GigabitEthernet2.12', '172.16.12.254', '120'),
                             ('GigabitEthernet2.13', '172.16.13.254', '120'),
                             ])
    for line in output:
        print(line)

    # ADVERTISE NETWORKS TO BGP

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

    # CONFIGURE FIREWALL PORTS

    output = configure_fortigate_port(firewall="10.10.99.1", username="admin", password="cisco123", 
                             port="port2", ip="172.16.21.1", mask="255.255.255.0", 
                             mgmt_access=["ssh", "ping"], alias="inside", 
                             role="lan", status="up")
    for line in output:
        print(line)

    # ADVERTISE NETWORKS TO BGP ON FIREWALL

    if configure_fortigate_bgp("10.10.99.1", "admin", "cisco123"):
        print("Connected interfaces advertised successfully!")

    # CREATE FIRWEALL POLICY OBJECTS - ADDRESSES

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

    # CONFIGURE FIREWALL POLICY

    output = configure_fortigate_fw_policy("10.10.99.1",
                                            username="script",
                                            password="cisco123",
                                            policy_name="inside-outside",
                                            src_int="port2",
                                            dest_int="port1",
                                            action="accept",
                                            src_address_group="ALLOW-ANY",
                                            dst_address_group="SITE1_ADDRESSES")
    for line in output:
        print(line)

    # CONFIGURE SVIs on SITE 2 SWITCHES

    output = configure_vlan_and_svi("10.10.99.2", "script", "cisco123", "10",
                                ["Ethernet0/0", "Ethernet0/2"], True, "172.16.21.2", "255.255.255.0")
    for line in output:
        print(line)

    
    output = create_static_route("10.10.99.2", "script", "cisco123",
                                 "0.0.0.0", "0.0.0.0", "172.16.21.1")
    for line in output:
        print(line)

    # TEST SITE 2 SITE CONNECTIVITY

    output = test_connectivity("10.10.99.2", "script", "cisco123",
                               source_ip="172.16.21.2", 
                               destination_ips=["172.16.11.1", "172.16.12.1", "172.16.13.1"])
    
    for line in output:
        print(line)