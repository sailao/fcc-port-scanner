import socket
import common_ports
import re

def portSCanner(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    if s.connect_ex((host, port)):
        s.close()
        return False
    else:
        s.close()
        return True

def verboseRespond(ip, ports = []):
    title = f"Open ports for {ip}"
    body = f"PORT     SERVICE\n"
    for index, port in enumerate(ports):
        service = common_ports.ports_and_services[port]
        body += str(port).ljust(4) + "     " + service
        if len(ports) != 1 and len(ports) != index + 1: body += "\n"
    
    return f"{title}\n{body}"

def get_open_ports(target, port_range, verbose = False):
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror as e:
        if (e.errno == 8 or e.errno == -2) and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
            return 'Error: Invalid IP address'
        else:
            return 'Error: Invalid hostname'

    try:
        domain = socket.gethostbyaddr(target)[0]
        ip = f"{domain} ({ip})"
    except socket.herror as e:
        if e.errno == 1:
            print('IP address has no DNS record')

    open_ports = []

    fromPort = port_range[0]

    if len(port_range) == 2:
        toPort = port_range[1]
    else:
        toPort = fromPort

    toPort = toPort + 1
    for port in range(fromPort, toPort):
        port = int(port)
        
        result = portSCanner(target, port)
        if result: open_ports.append(port)

    if verbose : return verboseRespond(ip, open_ports)

    return(open_ports)