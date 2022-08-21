from aiohttp import web
from http import HTTPStatus
import subprocess


access_tokens = [
    'telegram_bot'
]


def check_token(request) -> bool:
    token = request.rel_url.query.get('token')
    return token in access_tokens
     


async def create(request):
    if not check_token(request):
        return web.Response(status=HTTPStatus.UNAUTHORIZED)

    vpn_client = request.match_info['vpn_client']

    create_command = f"bash create_openvpn_client.sh {vpn_client}"
    process = subprocess.Popen(create_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return web.FileResponse(f"/root/vpn_configs/{vpn_client}.ovpn")


async def remove(request):
    if not check_token(request):
        return web.Response(status=HTTPStatus.UNAUTHORIZED)
    
    vpn_client = request.match_info['vpn_client']

    create_command = f"bash remove_openvpn_client.sh {vpn_client}"
    process = subprocess.Popen(create_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return web.Response(status=HTTPStatus.OK)