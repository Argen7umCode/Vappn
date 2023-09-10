import subprocess


class VPNConfig:
    def __init__(self, pubkey, privkey, name) -> None:
        self.pubkey = pubkey
        self.privkey = privkey
        self.name = name

    def __str__(self) -> str:
        return f'''[Interface]\nAddress = 10.9.0.1/24\nPrivateKey = {self.privkey}
[Peer]\nPublicKey = {self.pubkey}\nAllowedIPs = 10.9.0.2/32'''

    def save(self):
        with open(f'{self.name}.conf', 'w') as file:
            file.write(self)


class BashExecutor:
    def __init__(self):
        pass

    def execute(self, command):
        subprocess.run(command)


class VPN_manager(BashExecutor):
    def __init__(self):
        pass

    def __get_privkey(self):
        return self.execute(['wg', 'genkey'])
    
    def __get_pubkey(self, privkey):
        return self.execute(['echo', privkey, '|', 'wg', 'genkey'])

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
        return VPNConfig(server_privkey, client_pubkey)

    def delete_config(self, Config):
        

manager = VPN_manager()
