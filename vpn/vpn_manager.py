import os
import subprocess
from pprint import pprint

class VPNConfig:
    def __init__(self, pubkey, privkey, name) -> None:
        self.pubkey = pubkey
        self.privkey = privkey
        self.name = name

    def __str__(self) -> str:
        conf_str = \
        f'[Interface]\n' + \
        'Address = 10.9.0.1/24\n' + \
        f'PrivateKey = {self.privkey}' + \
        '[Peer]\n' + \
        f'PublicKey = {self.pubkey}' + \
        'AllowedIPs = 10.9.0.2/32'
        return conf_str

    def save(self):
        with open(f'{self.name}.conf', 'w') as file:
            file.write(str(self))


class BashExecutor:
    def __init__(self):
        pass

    def execute(self, command):
        return subprocess.run(command, stdout=subprocess.PIPE, text=True)


class VPNmanager(BashExecutor):
    def __init__(self):
        pass

    def __get_privkey(self):
        key = self.execute(['bash', 'private_key.sh']).stdout
        return key
    
    def __get_pubkey(self, privkey):
        return self.execute(['bash', 'public_key.sh', f'{privkey}']).stdout

    def __get_priv_pub_keys(self):
        privkey = self.__get_privkey()
        pubkey = self.__get_pubkey(privkey)

        return privkey, pubkey

    def __get_config_keys(self):
        server_privkey, server_pubkey = self.__get_priv_pub_keys()
        client_privkey, client_pubkey = self.__get_priv_pub_keys()
        return server_privkey, server_pubkey, client_privkey, client_pubkey

    def make_and_get_config(self, config_name):
        server_privkey, _, _, client_pubkey = self.__get_config_keys()
        config = VPNConfig(server_privkey, client_pubkey, config_name)
        config.save()
        return config

    def delete_config(self, Config):
        pass

