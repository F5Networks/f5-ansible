pipeline {
  agent {
    docker {
      image 'quay-gold'
    }
    
  }
  stages {
    stage('Checkout') {
      steps {
        git(url: 'git.com/sds', branch: 'master')
      }
    }
    stage('Functional') {
      steps {
        parallel(
          "bigip_vlan": {
            ansiblePlaybook 'bigip_vlan.yaml'
            
          },
          "bigip_selfip": {
            ansiblePlaybook 'bigip_selfip.yaml'
            
          },
          "bigip_static_route": {
            ansiblePlaybook(playbook: 'bigip_static_route', colorized: true)
            
          }
        )
      }
    }
    stage('Coverage') {
      steps {
        sh '''#!/bin/bash

run coverage'''
      }
    }
  }
}