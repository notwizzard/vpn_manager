client_name=$1
docker-compose run --rm openvpn ovpn_revokeclient "$client_name" remove