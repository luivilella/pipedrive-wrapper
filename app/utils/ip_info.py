import requests


def get_ip_info(ip):
    data = {}
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
    except requests.exceptions.ConnectionError:
        pass
    return data
