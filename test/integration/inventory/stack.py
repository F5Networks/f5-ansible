#!/usr/bin/env python

import argparse
import collections
import os
import time
from distutils.version import StrictVersion

try:
    import json
except:
    import simplejson as json

import os_client_config
import shade
import shade.inventory

CONFIG_FILES = ['/etc/ansible/openstack.yaml', '/etc/ansible/openstack.yml']


def get_groups_from_server(server_vars, namegroup=True):
    groups = []

    region = server_vars['region']
    cloud = server_vars['cloud']
    metadata = server_vars.get('metadata', {})

    # Create a group for the cloud
    groups.append(cloud)

    # Create a group on region
    groups.append(region)

    # And one by cloud_region
    groups.append("%s_%s" % (cloud, region))

    # Check if group metadata key in servers' metadata
    if 'group' in metadata:
        groups.append(metadata['group'])

    for extra_group in metadata.get('groups', '').split(','):
        if extra_group:
            groups.append(extra_group.strip())

    groups.append('instance-%s' % server_vars['id'])
    if namegroup:
        groups.append(server_vars['name'])

    for key in ('flavor', 'image'):
        if 'name' in server_vars[key]:
            groups.append('%s-%s' % (key, server_vars[key]['name']))

    for key, value in iter(metadata.items()):
        groups.append('meta-%s_%s' % (key, value))
    groups.append('f5-test')
    groups.append('bigip')

    az = server_vars.get('az', None)
    if az:
        # Make groups for az, region_az and cloud_region_az
        groups.append(az)
        groups.append('%s_%s' % (region, az))
        groups.append('%s_%s_%s' % (cloud, region, az))
    return groups


def get_host_groups(inventory, refresh=False):
    groups = to_json(get_host_groups_from_cloud(inventory))
    return groups


def append_hostvars(hostvars, groups, key, server, namegroup=False):
    hostvars[key] = dict(
        ansible_ssh_host=server['interface_ip'],
        ansible_host=server['interface_ip'],
        openstack=server)
    for group in get_groups_from_server(server, namegroup=namegroup):
        groups[group].append(key)


def get_host_groups_from_cloud(inventory):
    groups = collections.defaultdict(list)
    firstpass = collections.defaultdict(list)
    hostvars = {}
    list_args = {}
    if hasattr(inventory, 'extra_config'):
        use_hostnames = inventory.extra_config['use_hostnames']
        list_args['expand'] = inventory.extra_config['expand_hostvars']
        if StrictVersion(shade.__version__) >= StrictVersion("1.6.0"):
            list_args['fail_on_cloud_config'] = \
                inventory.extra_config['fail_on_errors']
    else:
        use_hostnames = False

    for server in inventory.list_hosts(**list_args):

        if 'interface_ip' not in server:
            continue
        firstpass[server['name']].append(server)
    for name, servers in firstpass.items():
        if len(servers) == 1 and use_hostnames:
            append_hostvars(hostvars, groups, name, servers[0])
        else:
            server_ids = set()
            # Trap for duplicate results
            for server in servers:
                server_ids.add(server['id'])
            if len(server_ids) == 1 and use_hostnames:
                append_hostvars(hostvars, groups, name, servers[0])
            else:
                for server in servers:
                    append_hostvars(
                        hostvars, groups, server['id'], server,
                        namegroup=True)
    groups['_meta'] = {'hostvars': hostvars}
    return groups


def is_cache_stale(cache_file, cache_expiration_time, refresh=False):
    ''' Determines if cache file has expired, or if it is still valid '''
    if refresh:
        return True
    if os.path.isfile(cache_file) and os.path.getsize(cache_file) > 0:
        mod_time = os.path.getmtime(cache_file)
        current_time = time.time()
        if (mod_time + cache_expiration_time) > current_time:
            return False
    return True


def to_json(in_dict):
    return json.dumps(in_dict, sort_keys=True, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(description='OpenStack Inventory Module')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true',
                       help='List active servers')
    group.add_argument('--stack', help='List details about the specific stack')
    group.add_argument('--host', help='List details about the specific host')

    return parser.parse_args()


def get_instance_ids(outputs):
    result = []
    for munch in outputs:
        if 'instance_id' in munch['output_key']:
            if type(munch['output_value']) is list:
                for x in munch['output_value']:
                    result.append(x)
            else:
                result.append(munch['output_value'])
    return result


def main():
    args = parse_args()
    import sys
    try:
        config_files = os_client_config.config.CONFIG_FILES + CONFIG_FILES
        inventory_args = dict(
            config_files=config_files
        )

        inventory = shade.inventory.OpenStackInventory(**inventory_args)

        groups = collections.defaultdict(list)
        firstpass = collections.defaultdict(list)
        hostvars = {}
        use_hostnames = True
        cloud = shade.openstack_cloud(cloud='default')
        stack = cloud.get_stack(args.stack)
        instance_ids = get_instance_ids(stack['outputs'])
        list_hosts = [inventory.get_host(i) for i in instance_ids]

        for server in list_hosts:
            if 'interface_ip' not in server:
                continue
            firstpass[server['name']].append(server)
        for name, servers in firstpass.items():
            if len(servers) == 1 and use_hostnames:
                append_hostvars(hostvars, groups, name, servers[0])
            else:
                server_ids = set()
                # Trap for duplicate results
                for server in servers:
                    server_ids.add(server['id'])
                if len(server_ids) == 1 and use_hostnames:
                    append_hostvars(hostvars, groups, name, servers[0])
                else:
                    for server in servers:
                        append_hostvars(
                            hostvars, groups, server['id'], server,
                            namegroup=True)
        groups['_meta'] = {'hostvars': hostvars}
        output = to_json(groups)
        print(output)
    except shade.OpenStackCloudException as e:
        sys.stderr.write('%s\n' % e.message)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
