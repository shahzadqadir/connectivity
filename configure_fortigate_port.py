# ~/automation/connectivity/configure_fortigate_port.py

import paramiko
from connectivity import Connectivity

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


if __name__ == "__main__":

    output = configure_fortigate_port(firewall="10.10.99.1", username="admin", password="cisco123", 
                             port="port2", ip="172.16.21.1", mask="255.255.255.0", 
                             mgmt_access=["ssh", "ping"], alias="inside", 
                             role="lan", status="up")
    for line in output:
        print(line)
