from aiohttp import web
from http import HTTPStatus
import subprocess


access_tokens = [
    'telegram_bot'
]


def check_token(request) -> bool:
    token = request.rel_url.query.get('token')
    return token in access_tokens


def git_push(action, vpn_client):
    create_command = f"bash push_vpn_configs.sh {action} {vpn_client} &"
    process = subprocess.Popen(create_command.split(), shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
    output, error = process.communicate()


async def create(request):
    if not check_token(request):
        return web.Response(status=HTTPStatus.UNAUTHORIZED)

    vpn_client = request.match_info['vpn_client']

    create_command = f"bash create_openvpn_client.sh {vpn_client}"
    process = subprocess.Popen(create_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    git_push('add', vpn_client)
    return web.FileResponse(f"/root/vpn_configs/{vpn_client}.ovpn")


async def remove(request):
    if not check_token(request):
        return web.Response(status=HTTPStatus.UNAUTHORIZED)
    
    vpn_client = request.match_info['vpn_client']

    create_command = f"bash remove_openvpn_client.sh {vpn_client}"
    process = subprocess.Popen(create_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    git_push('rm', vpn_client)
    return web.Response(status=HTTPStatus.OK)