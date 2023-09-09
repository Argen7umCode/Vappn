#!/usr/bin/bash

SERVER_PRIVKEY=$( wg genkey )
SERVER_PUBKEY=$( echo $SERVER_PRIVKEY | wg pubkey )
CLIENT_PRIVKEY=$( wg genkey )
CLIENT_PUBKEY=$( echo $CLIENT_PRIVKEY | wg pubkey )

echo "[Interface]
Address = 10.9.0.1/24
PrivateKey = $SERVER_PRIVKEY
[Peer]
PublicKey = $CLIENT_PUBKEY
AllowedIPs = 10.9.0.2/32" >>  ./$1.conf
