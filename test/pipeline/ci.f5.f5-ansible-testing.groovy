/**
 * Copyright (c) 2017 F5 Networks Inc.
 * GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
 */

timestamps {
  node('openstack') {
    def modules = readYaml file: 'test/pipeline/ci.f5.f5-ansible-testing.modules.yaml'
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

    stage('Integration testing') {
      milestone(label: 'IntegrationTests-AttemptingToStart')
      timeout(240) {
        waitUntil {
          docker.withRegistry("${DOCKER_REGISTRY}") {
            docker.image("${DOCKER_IMAGE}").inside {
              dir('test/runner') {
                sh returnStatus: true,
                   script: """
                     ansible-playbook -i inventory/hosts playbooks/setup-harness.yaml \
                     -e harness=${HARNESS} -e harness_name=${HARNESS}-build.${BUILD_NUMBER}
                   """
                return (r == 0)
              }
            }
          }
        }
        waitUntil {
          environment {
            STACK_NAME = "${HARNESS}-build.${BUILD_NUMBER}"
          }
          docker.withRegistry("${DOCKER_REGISTRY}") {
            docker.image("${DOCKER_IMAGE}").inside {
              dir('test/integration') {
                for (module in modules['modules']) {

                  def yamlData = readYaml file: './test/integration/'
                  if !yamlData['vars']['__metadata__'].containsKey('tested_harnesses') {
                    currentBuild.result = 'SUCCESS'
                    return
                  }
                  isTestableInHarness = ${HARNESS} in yamlData['vars']['__metadata__']['tested_harnesses']
                  if (!isTestableInHarness) {
                    currentBuild.result = 'SUCCESS'
                    return
                  }

                  sh returnStatus: true,
                     script: """
                       ansible-playbook -i inventory/stack \
                       ${module}.yaml -e harness_name=${HARNESS}-build.${BUILD_NUMBER}"
                     """
                }
                return (r == 0)
              }
            }
          }
        }
        waitUntil {
          docker.withRegistry("${DOCKER_REGISTRY}") {
            docker.image("${DOCKER_IMAGE}").inside {
              dir('test/runner') {
                sh returnStatus: true,
                   script: """
                     ansible-playbook -i inventory/hosts playbooks/teardown-harness.yaml \
                     -e harness_name=${HARNESS}-build.${BUILD_NUMBER}
                   """
                return (r == 0)
              }
            }
          }
        }
      }
      milestone(label: 'IntegrationTests-Done')
    }
  }
}
