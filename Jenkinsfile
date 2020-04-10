pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:buster' 
                }
            }
            steps {
                sh 'python -m py_compile anagram.py main.py' 
            }
        }
    }
}