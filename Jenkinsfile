pipeline {
agent any

stages {

    stage('Checkout') {
        steps {
            git branch: 'master',
                url: 'https://github.com/sanjusubramani/CICD_2.git'
        }
    }

    stage('Create Virtual Environment') {
        steps {
            dir('my_python_app') {
                sh 'python3 -m venv venv'
            }
        }
    }

    stage('Install Dependencies') {
        steps {
            dir('my_python_app') {
                sh '''
                venv/bin/pip install --upgrade pip
                venv/bin/pip install -r requirements.txt
                '''
            }
        }
    }

    stage('Unit Tests') {
        steps {
            dir('my_python_app') {
                sh 'venv/bin/python -m unittest discover tests'
            }
        }
    }

    stage('SonarQube Analysis') {
        steps {
            dir('my_python_app') {
                withSonarQubeEnv('SonarQube') {
                    withCredentials([
                        string(
                            credentialsId: 'sonar_token',
                            variable: 'SONAR_TOKEN'
                        )
                    ]) {
                        sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=my_python_app \
                        -Dsonar.sources=. \
                        -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }
    }

    stage('Quality Gate') {
        steps {
            timeout(time: 5, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
        }
    }

    stage('Docker Login') {
        steps {
            withCredentials([
                usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )
            ]) {
                sh '''
                echo $DOCKER_PASS | docker login \
                -u $DOCKER_USER \
                --password-stdin
                '''
            }
        }
    }

    stage('Docker Build') {
        steps {
            dir('my_python_app') {
                sh '''
                docker build \
                -t sanju2024/python-fn-web-app:${BUILD_NUMBER} .
                '''
            }
        }
    }

    stage('Docker Push') {
        steps {
            sh '''
            docker push \
            sanju2024/python-fn-web-app:${BUILD_NUMBER}
            '''
        }
    }

    stage('Deploy to EC2') {
        steps {
            sshagent(credentials: ['ec2-key']) {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@18.140.113.219 << EOF

                docker pull sanju2024/python-fn-web-app:${BUILD_NUMBER}

                docker stop streamlit-app || true
                docker rm streamlit-app || true

                docker run -d \
                --name streamlit-app \
                -p 8501:8501 \
                sanju2024/python-fn-web-app:${BUILD_NUMBER}

                EOF
                '''
            }
        }
    }

    stage('Health Check') {
        steps {
            sshagent(credentials: ['ec2-key']) {
                sh '''
                sleep 20

                ssh -o StrictHostKeyChecking=no ubuntu@18.140.113.219 \
                "curl -f http://localhost:8501/_stcore/health"
                '''
            }
        }
    }
}

post {

    success {
        echo 'Pipeline executed successfully'
    }

    failure {
        echo 'Pipeline failed'
    }

    always {
        cleanWs()
    }
}
```

}
