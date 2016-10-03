Network Modules
```````````````

.. toctree:: :maxdepth: 1


F5
--

.. toctree:: :maxdepth: 1

  bigip_command (E) - Run commands on a BIG-IP via tmsh <bigip_command_module>
  bigip_device_dns (E) - Manage BIG-IP device DNS settings <bigip_device_dns_module>
  bigip_device_ntp (E) - Manage NTP servers on a BIG-IP <bigip_device_ntp_module>
  bigip_device_sshd (E) - Manage the SSHD settings of a BIG-IP <bigip_device_sshd_module>
  bigip_dns_record (E) - Manage DNS resource records on a BIG-IP <bigip_dns_record_module>
  bigip_dns_record_facts (E) - foo <bigip_dns_record_facts_module>
  bigip_dns_zone (E) - Manages DNS zones on a BIG-IP <bigip_dns_zone_module>
  bigip_facts (E) - Collect facts from F5 BIG-IP devices <bigip_facts_module>
  bigip_gtm_datacenter (E) - Manage Datacenter configuration in BIG-IP <bigip_gtm_datacenter_module>
  bigip_gtm_facts (E) - Collect facts from F5 BIG-IP GTM devices <bigip_gtm_facts_module>
  bigip_gtm_virtual_server (E) - Manages F5 BIG-IP GTM virtual servers <bigip_gtm_virtual_server_module>
  bigip_gtm_wide_ip (E) - Manages F5 BIG-IP GTM wide ip <bigip_gtm_wide_ip_module>
  bigip_hostname (E) - Manage the hostname of a BIG-IP <bigip_hostname_module>
  bigip_iapp_service (E) - foo <bigip_iapp_service_module>
  bigip_iapp_template (E) - foo <bigip_iapp_template_module>
  bigip_irule (E) - Manage iRules across different modules on a BIG-IP. <bigip_irule_module>
  bigip_license (E) - Manage license installation and activation on BIG-IP devices <bigip_license_module>
  bigip_monitor_http (E) - Manages F5 BIG-IP LTM http monitors <bigip_monitor_http_module>
  bigip_monitor_tcp (E) - Manages F5 BIG-IP LTM tcp monitors <bigip_monitor_tcp_module>
  bigip_node (E) - Manages F5 BIG-IP LTM nodes <bigip_node_module>
  bigip_partition (E) - Manage BIG-IP partitions <bigip_partition_module>
  bigip_pool (E) - Manages F5 BIG-IP LTM pools <bigip_pool_module>
  bigip_pool_member (E) - Manages F5 BIG-IP LTM pool members <bigip_pool_member_module>
  bigip_provision (E) - Manage BIG-IP module provisioning <bigip_provision_module>
  bigip_routedomain (E) - Manage route domains on a BIG-IP <bigip_routedomain_module>
  bigip_routedomain_facts (E) - Retrieve route domain attributes from a BIG-IP <bigip_routedomain_facts_module>
  bigip_selfip (E) - Manage Self-IPs on a BIG-IP system <bigip_selfip_module>
  bigip_service (E) - Manage BIG-IP service states <bigip_service_module>
  bigip_snmp (E) - foo <bigip_snmp_module>
  bigip_software (E) - Manage BIG-IP software versions and hotfixes <bigip_software_module>
  bigip_software_update (E) - Manage the software update settings of a BIG-IP <bigip_software_update_module>
  bigip_ssl_certificate (E) - Import/Delete certificates from BIG-IP <bigip_ssl_certificate_module>
  bigip_sys_db (E) - Manage BIG-IP system database variables <bigip_sys_db_module>
  bigip_sys_global (E) - Manage BIG-IP global settings <bigip_sys_global_module>
  bigip_ucs (E) - Manage UCS files <bigip_ucs_module>
  bigip_ucs_fetch (E) - Fetches a UCS file from remote nodes <bigip_ucs_fetch_module>
  bigip_user (E) - Manage user accounts and user attributes on a BIG-IP. <bigip_user_module>
  bigip_user_facts (E) - Retrieve user account attributes from a BIG-IP <bigip_user_facts_module>
  bigip_view (E) - Manage ZoneRunner Views on a BIG-IP <bigip_view_module>
  bigip_virtual_server (E) - Manages F5 BIG-IP LTM virtual servers <bigip_virtual_server_module>
  bigip_vlan (E) - Manage VLANs on a BIG-IP system <bigip_vlan_module>



.. note::
    -  (D): This marks a module as deprecated, which means a module is kept for backwards compatibility but usage is discouraged.  The module documentation details page may explain more about this rationale.
    -  (E): This marks a module as 'extras', which means it ships with ansible but may be a newer module and possibly (but not necessarily) less actively maintained than 'core' modules.
    - Tickets filed on modules are filed to different repos than those on the main open source project. Core module tickets should be filed at `ansible/ansible-modules-core on GitHub <http://github.com/ansible/ansible-modules-core>`_, extras tickets to `ansible/ansible-modules-extras on GitHub <http://github.com/ansible/ansible-modules-extras>`_
