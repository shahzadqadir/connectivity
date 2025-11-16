# ~/automation/connectivity/connectivity.py

import paramiko
import getpass
import time

class Connectivity:

    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.connection = None
        self.is_authenticated = False

    def __str__(self):
        return self.ip_address
    
    
    
    def login(self, username: str, password: str):
        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection.connect(hostname=self.ip_address, 
                                    username=username,
                                    password=password,
                                    allow_agent=False, 
                                    look_for_keys=False)
            self.is_authenticated = True

        except paramiko.ssh_exception.AuthenticationException:
            print("Invalid username/password")
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("Could not connect to device, Invalid certificates")

    def execute_show_commands(self, command: str):
        self.check_connection()
        stdin, stdout, stderr = self.connection.exec_command(command)
        command_output = stdout.readlines()
        command_output = [line.strip() for line in command_output]
        return command_output

    def config_cmd_ssh(self, cmd_list: list) -> bool:
        self.check_connection()
        remote_conn = self.connection.invoke_shell()
        for command in cmd_list:
            remote_conn.send(command + '\n')
            time.sleep(0.5)
        remote_conn.close()
        self.connection = None
        return True

    def check_connection(self):
        if self.connection is None:
            self.login(username=input("Username: "), password=getpass.getpass("Password: "))
        else:
            pass

    @classmethod
    def print_to_screen(cls, output: list):
        for item in output:
            print(item)
            
    @classmethod
    def print_to_file(cls, output: list, filename: str):
        with open(filename, "a") as file:            
            for item in output:
                file.write(item)
                file.write("\n")
            file.write("\n")

if __name__ == "__main__":
    connectivity = Connectivity("10.10.99.11")
    connectivity.config_cmd_ssh(["configure terminal", "interface loopback2", "ip address 200.0.0.2 255.255.255.0", "end"])
    print("Configuration completed.")
    print("Check list of interfaces!")
    output = connectivity.execute_show_commands("show ip int brief")
    Connectivity.print_to_screen(output)