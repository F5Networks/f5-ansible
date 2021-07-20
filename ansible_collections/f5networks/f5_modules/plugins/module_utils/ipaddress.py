# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    validate_ip_address, validate_ip_v6_address
)

from ipaddress import ip_interface, ip_network

IPV4_REGEX = r'(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}' \
            + r'([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])' \
            + r'(%[\w]+)?'

IPV4 = re.compile(IPV4_REGEX)

IPV6_REGEX = r'((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}' \
            + r'((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|' \
            + r'(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3}' \
            + r'(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))' \
            + r'(%[\w]+)?'

IPV6 = re.compile(IPV6_REGEX)

ID = re.compile(r'%[\w]+')

def remove_ip_id(addr):
    if u'%' in addr:
        m = ID.search(addr)
        return addr[:m.start()] + addr[m.end():]


def is_valid_ip(addr, type='all'):
    if IPV4.match(addr):
        return True
    if IPV6.match(addr):
        return True
    return False


def ipv6_netmask_to_cidr(mask):
    """converts an IPv6 netmask to CIDR form

    According to the link below, CIDR is the only official way to specify
    a subset of IPv6. With that said, the same link provides a way to
    loosely convert an netmask to a CIDR.

    Arguments:
      mask (string): The IPv6 netmask to convert to CIDR

    Returns:
      int: The CIDR representation of the netmask

    References:
      https://stackoverflow.com/a/33533007
      http://v6decode.com/
    """
    bit_masks = [
        0, 0x8000, 0xc000, 0xe000, 0xf000, 0xf800,
        0xfc00, 0xfe00, 0xff00, 0xff80, 0xffc0,
        0xffe0, 0xfff0, 0xfff8, 0xfffc, 0xfffe,
        0xffff
    ]
    count = 0
    try:
        for w in mask.split(':'):
            if not w or int(w, 16) == 0:
                break
            count += bit_masks.index(int(w, 16))
        return count
    except Exception:
        return -1


def is_valid_ip_network(address):
    address = remove_ip_id(address)
    try:
        ip_network(u'{0}'.format(address))
        return True
    except ValueError:
        return False


def is_valid_ip_interface(address):
    address = remove_ip_id(address)
    if is_valid_ip(address):
        try:
            ip_interface(address)
            return True
        except ValueError:
            return False


def get_netmask(address):
    address = remove_ip_id(address)
    addr = ip_network(u'{0}'.format(address))
    netmask = addr.netmask.compressed
    return netmask


def compress_address(address):
    address = remove_ip_id(address)
    addr = ip_network(u'{0}'.format(address))
    result = addr.compressed.split('/')[0]
    return result
