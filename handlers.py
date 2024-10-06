from aiohttp import web
from http import HTTPStatus
import subprocess
import os


access_tokens = [
    'telegram_bot'
]
with_docker_compose = False


def check_token(request) -> bool:
    token = request.rel_url.query.get('token')
    return token in access_tokens


def git_push(action, vpn_client):
    push_command = f"bash push_vpn_configs.sh {action} {vpn_client}"
    process = subprocess.Popen(push_command.split(), shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
    output, error = process.communicate()


async def create(request):
    if not check_token(request):
        return web.Response(status=HTTPStatus.UNAUTHORIZED)

    vpn_client = request.match_info['vpn_client']

    script_name = "create_openvpn_client.sh" if not with_docker_compose \
        else "docker_compose_create_openvpn_client.sh"
    create_command = f"bash {script_name} {vpn_client}"
    process = subprocess.Popen(create_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # git_push('add', vpn_client)
    return web.FileResponse(f"/root/vpn_configs/{vpn_client}.ovpn")


async def remove(request):
    if not check_token(request):
        return web.Response(status=HTTPStatus.UNAUTHORIZED)
    
    vpn_client = request.match_info['vpn_client']

    script_name = "remove_openvpn_client.sh" if not with_docker_compose \
        else "docker_compose_remove_openvpn_client.sh"
    remove_command = f"bash {script_name} {vpn_client}"
    process = subprocess.Popen(remove_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # git_push('rm', vpn_client)
    return web.Response(status=HTTPStatus.OK)
