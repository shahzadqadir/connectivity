# ~/automation/connectivity/configure_fortigate_fw_policy.py

import paramiko
from connectivity import Connectivity

def configure_fortigate_fw_policy(firewall: str, username: str, password: str,
                                policy_name: str, src_int: str, dest_int: str,
                                action: str, src_address_group: str, 
                                dst_address_group: str, schedule: str="always", 
                                service: str="ALL", logg_traffic: str="all"):
    configurations = [
        "config firewall policy",
        "edit 1",
        f'set name {policy_name}',
        f'set srcintf {src_int}',
        f'set dstintf {dest_int}',
        f'set srcaddr {src_address_group}',
        f'set dstaddr {dst_address_group}',
        f'set action {action}',
        f'set schedule {schedule}',
        f'set service {service}',
        f'set logtraffic {logg_traffic}',
        "end"
    ]

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)

    connection = Connectivity(firewall)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show firewall policy")
    return output

if __name__ == "__main__":
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