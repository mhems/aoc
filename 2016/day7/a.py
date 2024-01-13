from sys import argv
import re

with open(argv[1]) as fp:
    lines = fp.readlines()

exclude_regex = re.compile(r'\[[^\]]*?\]')
abba_regex = re.compile(r'(.)(.)\2\1')

def supports_tls(ip: str) -> bool:
    for match in re.findall(exclude_regex, ip):
        if re.search(abba_regex, match):
            return False
    match = re.search(abba_regex, ip)
    if match:
        text = match.group(0)
        if text[0] != text[1]:
            return True
    return False

def supports_ssl(ip: str) -> bool:
    hypernets = ''.join(re.findall(exclude_regex, ip))
    ip = re.sub(exclude_regex, ',', ip)
    for i in range(len(ip) - 2):
        if ip[i + 2] == ip[i] and ip[i] != ip[i+1]:
            search = ip[i+1] + ip[i] + ip[i+1]
            if search in hypernets:
                return True
    return False

print(sum(int(supports_tls(ip.strip())) for ip in lines))
print(sum(int(supports_ssl(ip.strip())) for ip in lines))
