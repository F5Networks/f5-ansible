#!/usr/bin/python

# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class Noop(object):
    """Represent no-operation required

    This class is used in the Difference engine to specify when an attribute
    has not changed. Difference attributes may return an instance of this
    class as a means to indicate when the attribute has not changed.

    The Noop object allows attributes to be set to None when sending updates
    to the API. `None` is technically a valid value in some cases (it indicates
    that the attribute should be removed from the resource).
    """
    pass


def fqdn_name(partition, value):
    if value is not None and not value.startswith('/'):
        return '/{0}/{1}'.format(partition, value)
    return value


def cleanup_tokens(client):
    try:
        resource = client.api.shared.authz.tokens_s.token.load(
            name=client.api.icrs.token
        )
        resource.delete()
    except Exception:
        pass
