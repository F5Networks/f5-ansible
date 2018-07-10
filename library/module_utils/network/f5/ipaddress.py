# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


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
    except:
        return -1
