import paramiko
from .connectivity import Connectivity


def create_vlans(switches_list: list) -> bool:
    for switch in switches_list:
        connection = Connectivity(switch)
        connection.login("script", "cisco123")
        

