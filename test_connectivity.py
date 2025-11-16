# ~/automation/connectivity/test_connectivity.py

from connectivity import Connectivity


def test_connectivity(source_device: str, username: str, password: str,
                      source_ip: str, destination_ips: list):
    output =[]
    for destination in destination_ips:
        connection = Connectivity(source_device)
        connection.login(username=username, password=password)
        output.append(connection.execute_show_commands(
            f"ping {destination} source {source_ip}"
        ))
    return output

if __name__ == "__main__":

    # Site 2 to Site 1
    output = test_connectivity("10.10.99.2", "script", "cisco123",
                               source_ip="172.16.21.2", 
                               destination_ips=["172.16.11.1", "172.16.12.1", "172.16.13.1"])
    
    for line in output:
        print(line)