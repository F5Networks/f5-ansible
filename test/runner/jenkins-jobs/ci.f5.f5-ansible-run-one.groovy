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

modules = [
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

def transformIntoModuleStep(module) {
  return {
    waitUntil {
      Random random = new Random()
      sleep time: random.nextInt(30), unit: 'SECONDS'
      dir('test/runner') {
        sh script: """
          docker-compose -f devtools/docker-compose.yaml run --rm \
              --name ${harness}-build.${BUILD_NUMBER} py2.7.10 \
              ansible-playbook -i inventory/hosts playbooks/teardown-harness.yaml \
              -e harness_name=${harness}-build.${BUILD_NUMBER}
        """, returnStatus: true
        return (r == 0)
      }
    }
  }
}

def transformIntoHarnessStep(harness) {
  return {
    timeout(240) {
      waitUntil {
        Random random = new Random()
        sleep time: random.nextInt(30), unit: 'SECONDS'
        dir('test/runner') {
          sh script: """
            docker-compose -f devtools/docker-compose.yaml run --rm \
                --name ${harness}-build.${BUILD_NUMBER} py2.7.10 \
                ansible-playbook -i inventory/hosts playbooks/setup-harness.yaml \
                -e harness=${harness} -e harness_name=${harness}-build.${BUILD_NUMBER}
          """, returnStatus: true
          return (r == 0)
        }
      }

      def stepsForParallel = modules.collectEntries {
        ["${it}" : transformIntoModuleStep(it)]
      }
      parallel stepsForParallel

      waitUntil {
        Random random = new Random()
        sleep time: random.nextInt(30), unit: 'SECONDS'
        dir('test/runner') {
          sh script: """
            docker-compose -f devtools/docker-compose.yaml run --rm \
                --name ${harness}-build.${BUILD_NUMBER} py2.7.10 \
                ansible-playbook -i test/infra/inventory/hosts test/infra/playbooks/teardown-harness.yaml \
                -e harness_name=${harness}-build.${BUILD_NUMBER}
          """, returnStatus: true
          return (r == 0)
        }
      }
    }
  }
}

timestamps {
    node('master') {
        milestone(label: 'Job-AttemptingToStart')
        cleanWs()

        stage('Checkout') {
            milestone(label: 'Checkout-AttemptingToStart')
            lock(resource: 'checkout-${env.BRANCH_NAME}', inversePrecedence: true) {
                git url: "https://github.com/F5Networks/f5-ansible.git"
            }
            milestone(label: 'Checkout-Done')
        }

        stage('Integration testing ') {
            milestone(label: 'IntegrationTests-AttemptingToStart')

            def stepsForParallel = harnesses.collectEntries {
                ["${it}" : transformIntoHarnessStep(it)]
            }
            parallel stepsForParallel

            milestone(label: 'IntegrationTests-Done')
        }
    }
}
