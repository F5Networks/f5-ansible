==============================================
F5Networks F5_Modules Collection Release Notes
==============================================

.. contents:: Topics


v1.1.0
======

Minor Changes
-------------

- Add accounting parameter for tacacs type to bigip_device_auth module
- Add fw_enforcement_policy parameter to bigip_selfip module
- Add persist cookie option to bigip_policy_rule module
- Add phase1_lifetime parameter to bigip_ike_peer module
- Add self allow option to bigip_network_globals module
- Add true_names support to bigip_profile_client_ssl modules allowing specifying true filenames of the certificates
- New ftp monitor module for configuring and managing ftp monitors
- New icmp monitor module for configuring and managing icmp monitors
- New smtp monitor module for configuring and managing smtp monitors
- New universal persistence profile module for configuring and managing universal persistence profiles

Deprecated Features
-------------------

- Deprecated bigip_appsvcs_extension module
- Deprecated bigip_device_facts module name
- Deprecated bigiq_device_facts module name

Removed Features (previously deprecated)
----------------------------------------

- Remove _bigip_iapplx_package alias
- Remove _bigip_security_address_list alias
- Remove _bigip_security_port_list alias
- Remove _bigip_traffic_group alias
- Remove bigip_asm_policy module

Bugfixes
--------

- Fix allowing authenticated not authorized users using modules to modify a resource
- Fix ipv6 netmask for self-ips in bigip_device_info
- Fix save_when parameter not saving configuration as expected in bigip_imish_config module

New Modules
-----------

- bigip_monitor_ftp - Manage FTP monitors on a BIG-IP
- bigip_monitor_icmp - Manages F5 BIG-IP LTM ICMP monitors
- bigip_monitor_smtp - Manage SMTP monitors on a BIG-IP
- bigip_profile_persistence_universal - Manage universal persistence profiles

v1.0.0
======

New Plugins
-----------

Lookup
~~~~~~

- bigiq_license - Return random license from list
- license_hopper - Return random license from list

New Modules
-----------

- bigip_apm_acl - Manage user-defined APM ACLs
- bigip_apm_network_access - Manage APM Network Access resource
- bigip_apm_policy_fetch - Exports the APM policy or APM access profile from remote nodes.
- bigip_apm_policy_import - Manage BIG-IP APM policy or APM access profile imports
- bigip_asm_dos_application - Manage application settings for DOS profile
- bigip_asm_policy_fetch - Exports the asm policy from remote nodes.
- bigip_asm_policy_import - Manage BIG-IP ASM policy imports
- bigip_asm_policy_manage - Manage BIG-IP ASM policies
- bigip_asm_policy_server_technology - Manages Server Technology on ASM policy
- bigip_asm_policy_signature_set - Manages Signature Sets on ASM policy
- bigip_cgnat_lsn_pool - Manage CGNAT LSN Pools
- bigip_cli_alias - Manage CLI aliases on a BIG-IP
- bigip_cli_script - Manage CLI scripts on a BIG-IP
- bigip_command - Run TMSH and BASH commands on F5 devices
- bigip_config - Manage BIG-IP configuration sections
- bigip_configsync_action - Perform different actions related to config-sync
- bigip_data_group - Manage data groups on a BIG-IP
- bigip_device_auth - Manage system authentication on a BIG-IP
- bigip_device_auth_ldap - Manage LDAP device authentication settings on BIG-IP
- bigip_device_certificate - Manage self-signed device certificates
- bigip_device_connectivity - Manages device IP configuration settings for HA on a BIG-IP
- bigip_device_dns - Manage BIG-IP device DNS settings
- bigip_device_group - Manage device groups on a BIG-IP
- bigip_device_group_member - Manages members in a device group
- bigip_device_ha_group - Manage HA group settings on a BIG-IP system
- bigip_device_httpd - Manage HTTPD related settings on BIG-IP
- bigip_device_info - Collect information from F5 BIG-IP devices
- bigip_device_license - Manage license installation and activation on BIG-IP devices
- bigip_device_ntp - Manage NTP servers on a BIG-IP
- bigip_device_sshd - Manage the SSHD settings of a BIG-IP
- bigip_device_syslog - Manage system-level syslog settings on BIG-IP
- bigip_device_traffic_group - Manages traffic groups on BIG-IP
- bigip_device_trust - Manage the trust relationships between BIG-IPs
- bigip_dns_cache_resolver - Manage DNS resolver cache configurations on BIG-IP
- bigip_dns_nameserver - Manage LTM DNS nameservers on a BIG-IP
- bigip_dns_resolver - Manage DNS resolvers on a BIG-IP
- bigip_dns_zone - Manage DNS zones on BIG-IP
- bigip_file_copy - Manage files in datastores on a BIG-IP
- bigip_firewall_address_list - Manage address lists on BIG-IP AFM
- bigip_firewall_dos_profile - Manage AFM DoS profiles on a BIG-IP
- bigip_firewall_dos_vector - Manage attack vector configuration in an AFM DoS profile
- bigip_firewall_global_rules - Manage AFM global rule settings on BIG-IP
- bigip_firewall_log_profile - Manages AFM logging profiles configured in the system
- bigip_firewall_log_profile_network - Configures Network Firewall related settings of the log profile
- bigip_firewall_policy - Manage AFM security firewall policies on a BIG-IP
- bigip_firewall_port_list - Manage port lists on BIG-IP AFM
- bigip_firewall_rule - Manage AFM Firewall rules
- bigip_firewall_rule_list - Manage AFM security firewall policies on a BIG-IP
- bigip_firewall_schedule - Manage BIG-IP AFM schedule configurations
- bigip_gtm_datacenter - Manage Datacenter configuration in BIG-IP
- bigip_gtm_global - Manages global GTM settings
- bigip_gtm_monitor_bigip - Manages F5 BIG-IP GTM BIG-IP monitors
- bigip_gtm_monitor_external - Manages external GTM monitors on a BIG-IP
- bigip_gtm_monitor_firepass - Manages F5 BIG-IP GTM FirePass monitors
- bigip_gtm_monitor_http - Manages F5 BIG-IP GTM http monitors
- bigip_gtm_monitor_https - Manages F5 BIG-IP GTM https monitors
- bigip_gtm_monitor_tcp - Manages F5 BIG-IP GTM tcp monitors
- bigip_gtm_monitor_tcp_half_open - Manages F5 BIG-IP GTM tcp half-open monitors
- bigip_gtm_pool - Manages F5 BIG-IP GTM pools
- bigip_gtm_pool_member - Manage GTM pool member settings
- bigip_gtm_server - Manages F5 BIG-IP GTM servers
- bigip_gtm_topology_record - Manages GTM Topology Records
- bigip_gtm_topology_region - Manages GTM Topology Regions
- bigip_gtm_virtual_server - Manages F5 BIG-IP GTM virtual servers
- bigip_gtm_wide_ip - Manages F5 BIG-IP GTM wide ip
- bigip_hostname - Manage the hostname of a BIG-IP
- bigip_iapp_service - Manages TCL iApp services on a BIG-IP
- bigip_iapp_template - Manages TCL iApp templates on a BIG-IP
- bigip_ike_peer - Manage IPSec IKE Peer configuration on BIG-IP
- bigip_imish_config - Manage BIG-IP advanced routing configuration sections
- bigip_interface - Module to manage BIG-IP physical interfaces.
- bigip_ipsec_policy - Manage IPSec policies on a BIG-IP
- bigip_irule - Manage iRules across different modules on a BIG-IP
- bigip_log_destination - Manages log destinations on a BIG-IP.
- bigip_log_publisher - Manages log publishers on a BIG-IP
- bigip_lx_package - Manages Javascript LX packages on a BIG-IP
- bigip_management_route - Manage system management routes on a BIG-IP
- bigip_message_routing_peer - Manage peers for routing generic message protocol messages
- bigip_message_routing_protocol - Manage generic message parser profile.
- bigip_message_routing_route - Manages static routes for routing message protocol messages
- bigip_message_routing_router - Manages router profiles for message-routing protocols
- bigip_message_routing_transport_config - Manages configuration for an outgoing connection
- bigip_monitor_dns - Manage DNS monitors on a BIG-IP
- bigip_monitor_external - Manages external LTM monitors on a BIG-IP
- bigip_monitor_gateway_icmp - Manages F5 BIG-IP LTM gateway ICMP monitors
- bigip_monitor_http - Manages F5 BIG-IP LTM http monitors
- bigip_monitor_https - Manages F5 BIG-IP LTM https monitors
- bigip_monitor_ldap - Manages BIG-IP LDAP monitors
- bigip_monitor_snmp_dca - Manages BIG-IP SNMP data collecting agent (DCA) monitors
- bigip_monitor_tcp_echo - Manages F5 BIG-IP LTM tcp echo monitors
- bigip_monitor_tcp_half_open - Manages F5 BIG-IP LTM tcp half-open monitors
- bigip_monitor_udp - Manages F5 BIG-IP LTM udp monitors
- bigip_network_globals - Manage network global settings on BIG-IP
- bigip_node - Manages F5 BIG-IP LTM nodes
- bigip_partition - Manage BIG-IP partitions
- bigip_password_policy - Manages the authentication password policy on a BIG-IP
- bigip_policy - Manage general policy configuration on a BIG-IP
- bigip_policy_rule - Manage LTM policy rules on a BIG-IP
- bigip_pool_member - Manages F5 BIG-IP LTM pool members
- bigip_profile_analytics - Manage HTTP analytics profiles on a BIG-IP
- bigip_profile_client_ssl - Manages client SSL profiles on a BIG-IP
- bigip_profile_dns - Manage DNS profiles on a BIG-IP
- bigip_profile_fastl4 - Manages Fast L4 profiles
- bigip_profile_ftp - Manages FTP profiles
- bigip_profile_http - Manage HTTP profiles on a BIG-IP
- bigip_profile_http2 - Manage HTTP2 profiles on a BIG-IP
- bigip_profile_http_compression - Manage HTTP compression profiles on a BIG-IP
- bigip_profile_oneconnect - Manage OneConnect profiles on a BIG-IP
- bigip_profile_persistence_cookie - Manage cookie persistence profiles on BIG-IP
- bigip_profile_persistence_src_addr - Manage source address persistence profiles
- bigip_profile_server_ssl - Manages server SSL profiles on a BIG-IP
- bigip_profile_sip - Manage SIP profiles on a BIG-IP
- bigip_profile_tcp - Manage TCP profiles on a BIG-IP
- bigip_profile_udp - Manage UDP profiles on a BIG-IP
- bigip_provision - Manage BIG-IP module provisioning
- bigip_qkview - Manage qkviews on the device
- bigip_remote_role - Manage remote roles on a BIG-IP
- bigip_remote_syslog - Manipulate remote syslog settings on a BIG-IP
- bigip_remote_user - Manages default settings for remote user accounts on a BIG-IP
- bigip_routedomain - Manage route domains on a BIG-IP
- bigip_selfip - Manage Self-IPs on a BIG-IP system
- bigip_service_policy - Manages service policies on a BIG-IP.
- bigip_smtp - Manages SMTP settings on the BIG-IP
- bigip_snat_pool - Manage SNAT pools on a BIG-IP
- bigip_snat_translation - Manage SNAT Translations on a BIG-IP
- bigip_snmp - Manipulate general SNMP settings on a BIG-IP
- bigip_snmp_community - Manages SNMP communities on a BIG-IP.
- bigip_snmp_trap - Manipulate SNMP trap information on a BIG-IP
- bigip_software_image - Manage software images on a BIG-IP
- bigip_software_install - Install software images on a BIG-IP
- bigip_software_update - Manage the software update settings of a BIG-IP
- bigip_ssl_certificate - Import/Delete certificates from BIG-IP
- bigip_ssl_key - Import/Delete SSL keys from BIG-IP
- bigip_ssl_ocsp - Manage OCSP configurations on BIG-IP
- bigip_static_route - Manipulate static routes on a BIG-IP
- bigip_sys_daemon_log_tmm - Manage BIG-IP tmm daemon log settings
- bigip_sys_db - Manage BIG-IP system database variables
- bigip_sys_global - Manage BIG-IP global settings
- bigip_timer_policy - Manage timer policies on a BIG-IP
- bigip_traffic_selector - Manage IPSec Traffic Selectors on BIG-IP
- bigip_trunk - Manage trunks on a BIG-IP
- bigip_tunnel - Manage tunnels on a BIG-IP
- bigip_ucs - Manage upload, installation and removal of UCS files
- bigip_ucs_fetch - Fetches a UCS file from remote nodes
- bigip_user - Manage user accounts and user attributes on a BIG-IP
- bigip_vcmp_guest - Manages vCMP guests on a BIG-IP
- bigip_virtual_address - Manage LTM virtual addresses on a BIG-IP
- bigip_virtual_server - Manage LTM virtual servers on a BIG-IP
- bigip_vlan - Manage VLANs on a BIG-IP system
- bigip_wait - Wait for a BIG-IP condition before continuing
- bigiq_application_fasthttp - Manages BIG-IQ FastHTTP applications
- bigiq_application_fastl4_tcp - Manages BIG-IQ FastL4 TCP applications
- bigiq_application_fastl4_udp - Manages BIG-IQ FastL4 UDP applications
- bigiq_application_http - Manages BIG-IQ HTTP applications
- bigiq_application_https_offload - Manages BIG-IQ HTTPS offload applications
- bigiq_application_https_waf - Manages BIG-IQ HTTPS WAF applications
- bigiq_device_discovery - Manage BIG-IP devices through BIG-IQ
- bigiq_device_info - Collect information from F5 BIG-IQ devices
- bigiq_regkey_license - Manages licenses in a BIG-IQ registration key pool
- bigiq_regkey_license_assignment - Manage regkey license assignment on BIG-IPs from a BIG-IQ
- bigiq_regkey_pool - Manages registration key pools on BIG-IQ
- bigiq_utility_license - Manage utility licenses on a BIG-IQ
- bigiq_utility_license_assignment - Manage utility license assignment on BIG-IPs from a BIG-IQ
