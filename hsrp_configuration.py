import paramiko
from connectivity import Connectivity


def configure_hsrp(router: str, username: str, password: str, 
                   svi_info: list) -> list:
    """ 
    svi_info format:
    [('sub-interface', 'virtual-ip', 'priority')]
    """
    configurations = ["configure terminal"]
    for line in svi_info:
        configurations.append(f"interface {line[0]}")
        configurations.append(f"standby 1 ip {line[1]}")
        configurations.append(f"standby 1 priority {line[2]}")
        configurations.append(f"standby 1 preempt")
    configurations.append("end")

    connection = Connectivity(router)
    connection.login(username=username, password=password)
    connection.config_cmd_ssh(configurations)
     # config_cmd_ssh closes connection so we need to open it again
    connection = Connectivity(router)
    connection.login(username=username, password=password)
    output = connection.execute_show_commands("show standby brief")
    return output


if __name__ == "__main__":
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
