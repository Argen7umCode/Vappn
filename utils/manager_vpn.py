import paramiko
import re
import os
from dotenv import load_dotenv
load_dotenv()

class ManagerVPN(paramiko.SSHClient):

    def __init__(self, ip, user, password) -> None:
        super().__init__()
        self.ip = ip 
        self.user = user
        self.password = password
        
    def create_connection(self):
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect(hostname=self.ip, username=self.user, password=self.password)

    def __clean_stdout_table(self, stdout):
        return [[item for item in line.split('  ') if item != ''] for line in stdout.read().decode("utf8").split('\n')[2:-2]]

    def __create_dict_from_stdout_table(self, stdout_table, columns):
        result = []
        for line in stdout_table:
            result.append({key : value for key, value in zip(columns, line)})
        return result

    def __make_response(self, command, columns):
        _, stdout, _ = self.exec_command(command)
        return self.__create_dict_from_stdout_table(self.__clean_stdout_table(stdout), columns)

    def get_clients_list(self):
        columns = ['client', 'public_key', 'creation_date']
        return self.__make_response('pivpn -l', columns)

    def get_clients_data(self):
        columns = ['name', 'remote_ip', 'virtual_ip', 'bytes_received', 'bytes_sent', 'last_seen']
        return self.__make_response('pivpn -c', columns)

    def add_client(self, name):
        _, stdout, _ = self.exec_command(f'pivpn -a -n {name}')
        stdout = str(stdout.read().decode('utf8'))
        if re.search(r'::: A client with this name already exists',  stdout):
            return False
        else:
            return True

    def get_config(self, name):
        _, stdout, _ = self.exec_command(f'cat /home/user/configs/{name}.conf')
        stdout = str(stdout.read().decode('utf8'))
        if re.search(r'No such file or directory', stdout):
            return None
        else:
            return stdout

    def register_new_client_and_get_config(self, name):
        if self.add_client(name):
            return self.get_config(name)
        else: 
            return None

    def remove_client(self, name):
        _, stdout, _ = self.exec_command(f'pivpn -r {name} -y')
        stdout = stdout.read().decode('utf8')
        if re.search(r'does not exist', stdout):
            return False
        else:
            return True

    def turn_off_or_client(self, name, on_off='on'):
        self.exec_command(f'pivpn -{on_off} {name} -y')