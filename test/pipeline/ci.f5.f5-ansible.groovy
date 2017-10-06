/**
 * Copyright 2017 F5 Networks Inc.
 *
 * This file is part of Ansible
 *
 * Ansible is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Ansible is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
 *
 * @author Tim Rupp <t.rupp@f5.com>
 */

// These containers must be named after the "services" that are in the
// docker-compose file.
containers = [
    'py2.7.10',
    'py3.5.4',
    'py3.6.2',
]

harnesses = [
    'TwoArmed-bigip-12.0.0',
    'TwoArmed-bigip-12.1.0',
    'TwoArmed-bigip-12.1.0-hf1',
    'TwoArmed-bigip-12.1.0-hf2',
    'TwoArmed-bigip-12.1.1',
    'TwoArmed-bigip-12.1.1-hf1',
    'TwoArmed-bigip-12.1.1-hf2',
    'TwoArmed-bigip-12.1.2',
    'TwoArmed-bigip-12.1.2-hf1',
    'TwoArmed-bigip-13.0.0',
    'TwoArmed-bigip-13.0.0-hf1',
]

/**
 * Do not manually edit this modules list. It is auto-generated
 * when you use the scripts/stubber.py script to stub and unstub
 * modules
 */
// STUBBER - START
modules = [
    'bigip_command.py',
    'bigip_config.py',
    'bigip_configsync_action.py',
    'bigip_device_connectivity.py',
    'bigip_device_dns.py',
    'bigip_device_group.py',
    'bigip_device_group_member.py',
    'bigip_device_ntp.py',
    'bigip_device_sshd.py',
    'bigip_device_trust.py',
    'bigip_dns_record.py',
    'bigip_dns_record_facts.py',
    'bigip_dns_zone.py',
    'bigip_drop_connection.py',
    'bigip_gtm_datacenter.py',
    'bigip_gtm_facts.py',
    'bigip_gtm_pool.py',
    'bigip_gtm_server.py',
    'bigip_gtm_virtual_server.py',
    'bigip_gtm_wide_ip.py',
    'bigip_hostname.py',
    'bigip_iapp_service.py',
    'bigip_iapp_template.py',
    'bigip_iapplx_package.py',
    'bigip_irule.py',
    'bigip_license.py',
    'bigip_monitor_http.py',
    'bigip_monitor_snmp_dca.py',
    'bigip_monitor_tcp.py',
    'bigip_monitor_tcp_echo.py',
    'bigip_monitor_tcp_half_open.py',
    'bigip_node.py',
    'bigip_partition.py',
    'bigip_policy.py',
    'bigip_policy_rule.py',
    'bigip_pool.py',
    'bigip_profile_client_ssl.py',
    'bigip_provision.py',
    'bigip_qkview.py',
    'bigip_raw.py',
    'bigip_remote_syslog.py',
    'bigip_routedomain.py',
    'bigip_routedomain_facts.py',
    'bigip_selfip.py',
    'bigip_service.py',
    'bigip_snat_pool.py',
    'bigip_snmp.py',
    'bigip_snmp_community.py',
    'bigip_snmp_trap.py',
    'bigip_snmp_user.py',
    'bigip_software.py',
    'bigip_software_facts.py',
    'bigip_software_update.py',
    'bigip_ssl_certificate.py',
    'bigip_ssl_key.py',
    'bigip_static_route.py',
    'bigip_sys_db.py',
    'bigip_sys_global.py',
    'bigip_ucs.py',
    'bigip_ucs_fetch.py',
    'bigip_user.py',
    'bigip_user_facts.py',
    'bigip_vcmp_guest.py',
    'bigip_view.py',
    'bigip_virtual_address.py',
    'bigip_virtual_server.py',
    'bigip_vlan.py',
    'bigiq_license_pool.py',
    'bigiq_license_pool_member.py',
    'f5_support_upload.py',
    'iworkflow_device.py',
    'iworkflow_iapp_template.py',
    'iworkflow_license.py',
    'iworkflow_license_pool.py',
    'iworkflow_license_pool_member.py',
    'iworkflow_local_connector.py',
    'iworkflow_local_connector_device.py',
    'iworkflow_local_connector_node.py',
    'iworkflow_service.py',
    'iworkflow_service_template.py',
    'iworkflow_system_setup.py',
    'iworkflow_tenant.py',
    'iworkflow_tenant_connector.py',
    'iworkflow_user.py',
    'wait_for_bigip.py',
]
// STUBBER - END

def transformIntoHarnessStep(harness) {
  /**
   * Provides a step for parallel testing of harnesses
   *
   * The step that this method returns can be thought of as,
   *
   * 1. Starting with a build steps
   * 2. Fanning out
   *
   * @param harness Harness to run integration tests on.
   * @param python_version Python version defined in docker-compose file.
   */
  return {
    timeout(240) {
      waitUntil {
        Random random = new Random()
        sleep time: random.nextInt(30), unit: 'SECONDS'
        docker.image('f5ansible/py2.7.10').inside {
          dir('test/runner') {
            sh script: """
                  ansible-playbook -i inventory/hosts playbooks/setup-harness.yaml \
                  -e harness=${harness} -e harness_name=${harness}-build.${BUILD_NUMBER}
            """, returnStatus: true
            return (r == 0)
          }
        }
      }

      /**
       * Tests need to happen across multiple containers, but cannot happen
       * in parallel because the integration tests have the possibility of stepping
       * on each other during setup and running.
       *
       * In a perfect world we boot a separate BIGIP VM instance for each container
       * that needs to run. See the `calculating-quota.rst` document in the F5
       * Ansible module documentation for the quota requirements
       */
      for (container in containers) {
          if (F5_MODULE == 'ALL') {
              for (module in modules) {
                  moduleStep(module, container)
              }
          } else {
              moduleStep(F5_MODULE, container)
          }
      }

      waitUntil {
        Random random = new Random()
        sleep time: random.nextInt(30), unit: 'SECONDS'
        docker.image('f5ansible/py2.7.10').inside {
          dir('test/runner') {
            sh script: """
                ansible-playbook -i inventory/hosts playbooks/teardown-harness.yaml \
                -e harness_name=${harness}-build.${BUILD_NUMBER}
            """, returnStatus: true
            return (r == 0)
          }
        }
      }
    }
  }
}

def moduleStep(module, container) {
  waitUntil {
    Random random = new Random()
    sleep time: random.nextInt(30), unit: 'SECONDS'
    environment {
        STACK_NAME = "${harness}-build.${BUILD_NUMBER}"
    }
    docker.image('f5ansible/${container}').inside {
      dir('test/integration') {
        sh script: "ansible-playbook -i inventory/stack ${module}.yaml -e harness_name=${harness}-build.${BUILD_NUMBER}",
           returnStatus: true
        return (r == 0)
      }
    }
  }
}

timestamps {
    node('openstack') {
        milestone(label: 'Job-AttemptingToStart')
        cleanWs()

        stage('Checkout') {
            milestone(label: 'Checkout-AttemptingToStart')
            lock(resource: 'checkout-${env.BRANCH_NAME}', inversePrecedence: true) {
                git url: "https://github.com/F5Networks/f5-ansible.git",
                    branch: 'devel'
            }
            milestone(label: 'Checkout-Done')
        }

        stage('Build') {
          sh "ls -l"
          sh "./devtools/bin/build-py2.7.10"
          sh "./devtools/bin/build-py3.5.4"
          sh "./devtools/bin/build-py3.6.2"
        }

        stage('Integration testing ') {
            milestone(label: 'IntegrationTests-AttemptingToStart')
            def stepsForParallel = harnesses.collectEntries {
                ["harness-${it}" : transformIntoHarnessStep(it)]
            }
            parallel stepsForParallel
            milestone(label: 'IntegrationTests-Done')
        }
    }
}
