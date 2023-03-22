import requests
import socket
import ssl
from urllib.parse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def string_similarity(str1, str2):
    distances = [[0 for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

    for i in range(len(str1) + 1):
        distances[i][0] = i
    for j in range(len(str2) + 1):
        distances[0][j] = j

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                distances[i][j] = distances[i - 1][j - 1]
            else:
                distances[i][j] = min(distances[i - 1][j], distances[i][j - 1], distances[i - 1][j - 1]) + 1

    return distances[-1][-1]


def is_redirect(link):
    response = requests.head(link, allow_redirects=False)
    return response.status_code in (301, 302)


def has_suspicious_js(link):
    response = requests.get(link)
    js_code = response.text
    return "eval(" in js_code or "document.location.replace(" in js_code


def is_solution(link):
    response = requests.get(link, verify=False)
    content_type = response.headers['content-type']
    return 'application/octet-stream' in content_type or '.exe' in link or '.dll' in link


def is_https(link):
    return link.startswith('https://')


def has_ssl_cert(link):
    response = requests.head(link)
    url = response.url
    if isinstance(url, bytes):
        url = url.decode('utf-8')
    domain = urlparse(url).netloc.split(':')[0]
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:
            cert = ssl_sock.getpeercert()
            return bool(cert)


def is_suspicious(link):
    flag = False
    domens = ['google', 'facebook', 'amazon', 'twitter', 'linkedin', 'youtube']
    parsed_link = urlparse(link)
    domain = parsed_link.netloc.split('.')[1]
    for i in domens:
        if 0 < string_similarity(domain, i) < 3:
            flag = True

    return flag


def is_long_level(link):
    return len(link.split('.')) > 4


def is_unreadable(link):
    return any(char in link for char in ['xn--', 'xn----', 'xn------'])


def check_link(link):
    print(link)
    stats = {
        'redirect': is_redirect(link),
        'https': is_https(link),
        'ssl': has_ssl_cert(link),
        'suspicious': is_suspicious(link),
        'Long level': is_long_level(link),
        'Unreadability': is_unreadable(link)
    }
    print(link)
    return stats
