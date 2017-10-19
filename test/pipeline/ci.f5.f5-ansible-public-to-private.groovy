node {
    cleanWs()
    docker.image('alpine/git:latest').inside {
        sh 'mkdir -p ~/.ssh'
        git branch: 'devel', url: 'https://github.com/F5Networks/f5-ansible.git'
        sh "git remote add downstream ${DOWNSTREAM_URL}"
        sshagent(["${CREDENTIAL_ID}"]) {
            sh "echo 'Host ${IGNORED_HOST}\n\tStrictHostKeyChecking no\n' >> ~/.ssh/config"
            sh 'git fetch downstream'
            sh 'git push downstream origin/devel:refs/heads/devel'
        }
    }
}
