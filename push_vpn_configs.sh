action=$1
client=$2

cd ~/vpn_configs/
git pull
git $action $client.ovpn
git commit -m "$acion client bash script"
git push