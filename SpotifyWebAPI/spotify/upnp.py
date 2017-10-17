# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import socket
import requests
import random
from urlparse import urlparse
from xml.dom.minidom import parseString, Document

SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 2
SSDP_ST = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"

_add_arguments = [
    ('NewExternalPort', '{port}'),            # specify port on router
    ('NewProtocol', 'TCP'),                   # specify protocol
    ('NewInternalPort', '{port}'),            # specify port on internal host
    ('NewInternalClient', '{internal_ip}'),   # specify IP of internal host
    ('NewEnabled', '1'),                      # turn mapping ON
    ('NewPortMappingDescription', 'Spotify'), # add a description
    ('NewLeaseDuration', '0')                 # how long should it be opened?
]

_remove_arguments = [
    ('NewRemoteHost', '{internal_ip}'),       # specify IP of internal host
    ('NewExternalPort', '{port}'),            # specify port on router
    ('NewProtocol', 'TCP')                    # specify protocol
]

HEADER = {
    'SOAPAction': (
        '"urn:schemas-upnp-org:service:WANIPConnection:1#AddPortMapping"'
    ),
    'Content-Type': 'text/xml'
}

SSDP_REQUEST = (
    'M-SEARCH * HTTP/1.1\r\n'
    'HOST: %s:%d\r\n'
    'MAN: "ssdp:discover"\r\n'
    'MX: %d\r\n'
    'ST: %s\r\n'
    '\r\n' % (SSDP_ADDR, SSDP_PORT, SSDP_MX, SSDP_ST)
)

router = None
router_location = None
upnp_remove_request = None


def _find_router():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10)
    dest = socket.gethostbyname(SSDP_ADDR)
    sock.sendto(SSDP_REQUEST, (dest, SSDP_PORT))
    sock.settimeout(20)

    try:
        data = sock.recv(1000)
    except socket.timeout:
        pass
    else:

        response = data.decode('utf-8')
        # match = re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', response)

        location = list(
            line.lower().replace('location', '').strip()
            for line in response.text.split('\n')
            if line.strip().lower().startswith('location')
        )[0]

        router_path = urlparse(location)
        response = requests.get(location)
        dom = parseString(response.text)

        for service in dom.getElementsByTagName('serviceType'):
            if service.childNodes[0].data.find('WANIPConnection') > 0:
                global router
                router = router_path

                return service.parentNode.getElementsByTagName(
                    'controlURL'
                )[0].childNodes[0].data


def _build_add_request():
    document = Document()
    envelope = document.createElementNS('', 's:Envelope')
    envelope.setAttribute(
        'xmlns:s',
        'http://schemas.xmlsoap.org/soap/envelope/'
    )
    envelope.setAttribute(
        's:encodingStyle',
        'http://schemas.xmlsoap.org/soap/encoding/'
    )
    body = document.createElementNS('', 's:Body')
    command = document.createElementNS('', 'u:AddPortMapping')
    command.setAttribute(
        'xmlns:u',
        'urn:schemas-upnp-org:service:WANIPConnection:1'
    )

    for k, v in _add_arguments:
        command.appendChild(
            document.createElement(k).appendChild(document.createTextNode(v))
        )

    body.appendChild(command)
    envelope.appendChild(body)
    document.appendChild(envelope)
    return document.toxml()


def add_port_mapping(host=None, port=None):
    response = requests.get('https://api.ipify.org', params='format=json')
    external_ip = response.json()['ip']
    internal_ip = socket.gethostbyname(socket.gethostname())
    if port is None:
        port = random.randrange(45000, 65535)

    if host is not None:
        redirect_uri = 'http://%s:%s' % (host, port)
    else:
        redirect_uri = 'http://%s:%s' % (external_ip, port)

    if external_ip != internal_ip:
        global router_location

        router_location = _find_router()
        if router_location is not None:
            global upnp_remove_request

            upnp_add_request = _build_add_request().format(
                port=port,
                internal_ip=internal_ip
            )
            upnp_remove_request = _build_remove_request().format(
                port=port,
                internal_ip=internal_ip
            )

            if _send_request(upnp_add_request):
                return redirect_uri, 'Router Success'

        return redirect_uri, 'Router Failure'
    return redirect_uri, 'Router Unavailable'


def _send_request(request):

        response = requests.post(
            url='%s:%s%s' % (
                router.hostname,
                router.port,
                router_location
            ),
            data=request,
            headers=HEADER
        )

        return response.ok


def _build_remove_request():
    document = Document()
    envelope = document.createElementNS('', 's:Envelope')
    envelope.setAttribute(
        'xmlns:s',
        'http://schemas.xmlsoap.org/soap/envelope/'
    )
    envelope.setAttribute(
        's:encodingStyle',
        'http://schemas.xmlsoap.org/soap/encoding/'
    )
    body = document.createElementNS('', 's:Body')
    command = document.createElementNS('', 'u:DeletePortMapping')
    command.setAttribute(
        'xmlns:u',
        'urn:schemas-upnp-org:service:WANIPConnection:1'
    )

    for k, v in _remove_arguments:
        command.appendChild(
            document.createElement(k).appendChild(document.createTextNode(v))
        )

    body.appendChild(command)
    envelope.appendChild(body)
    document.appendChild(envelope)
    return document.toxml()


def remove_port_mapping():
    if router_location is None:
        return False

    return _send_request(upnp_remove_request)
