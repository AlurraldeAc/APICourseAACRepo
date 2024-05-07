pipeline {
    agent any

    stages {
        stage('python version') {
            steps {
              bat 'python --version'
            }
        }
        stage('Run Python Scripts') {
            steps {
                withPythonEnv('python3') {
                    bat 'pip install -r requirements.txt'
                    bat 'behave -f allure_behave.formatter:AllureFormatter -o reports/allure'
                }
            }
        }
        stage('reports') {
            steps {
                script {
                    allure ([
                        includeProperties: false,
                        jdk:'',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure']]
                    ])
                 }
            }
        }
    }
}