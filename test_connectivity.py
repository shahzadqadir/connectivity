# ~/automation/connectivity/test_connectivity.py

import paramiko
from connectivity import Connectivity


def test_connectivity(source_device: str, username: str, password: str,
                      source_ip: str, destination_ip: str):
    connection = Connectivity(source_device)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands(
                        f"ping {destination_ip} source {source_ip}")
    return output

if __name__ == "__main__":

    # Site 2 to Site 1
    output = test_connectivity("10.10.99.2", "script", "cisco123",
                               source_ip="172.16.21.2", 
                               destination_ip="172.16.11.1")
    for line in output:
        print(line)
    
    # Site 1 to Site 2
    output = test_connectivity("10.10.99.11", "script", "cisco123",
                               source_ip="172.16.11.1", 
                               destination_ip="172.16.21.2")
    for line in output:
        print(line)

