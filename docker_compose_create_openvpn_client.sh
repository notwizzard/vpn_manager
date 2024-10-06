client_name=$1
docker-compose run --rm openvpn easyrsa build-client-full "$client_name" nopass
docker-compose run --rm openvpn ovpn_getclient "$client_name" > ~/vpn_configs/"$client_name".ovpn