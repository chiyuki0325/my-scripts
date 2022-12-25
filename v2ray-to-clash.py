import yaml
import requests
from sys import argv
from base64 import b64decode
from urllib.parse import urlparse, ParseResult
import rapidjson as json


def parse_vmess(vmess_base64: str):
    try:
        vmess = json.loads(b64decode(vmess_base64.encode()).decode())
    except:
        print(vmess_base64)
    output = {
        'name': vmess['ps'],
        'type': 'vmess',
        'server': vmess['add'],
        'port': int(vmess['port']),
        'uuid': vmess['id'],
        'alterId': vmess['aid'],
        'cipher': 'auto'
    }
    if 'verify_cert' in vmess:
        output['skip-cert-verify'] = not vmess['verify_cert']
    if 'tls' in vmess:
        if vmess['tls'] == "":
            output['tls'] = False
        else:
            output['tls'] = True
    if 'net' in vmess:
        if vmess['net'] == 'ws':
            output['network'] = 'ws'
            ws_opts = {
                'path': vmess['path'],
                'headers': {
                    'Host': vmess['host']
                }
            }
            output['ws-opts'] = ws_opts
        elif vmess['net'] == 'tcp':
            output['network'] = 'tcp'
        else:
            return NotImplementedError(vmess['net'],vmess_base64)
    output['udp'] = True
    return output


proxies = []

proxy_links = b64decode(requests.get(argv[1]).text.encode()).decode().split('\n')  # 获取到的代理链接

for proxy_link in proxy_links:
    proxy = urlparse(proxy_link)
    if proxy.scheme == 'vmess':
        proxies.append(parse_vmess(proxy_link[8:]))
    else:
        print(proxy.scheme)
        NotImplementedError

print(yaml.dump(proxies))
