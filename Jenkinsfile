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
               sh 'venv/bin/pip install -r requirements.txt'
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

   stage('Build') {
       steps {
           dir('my_python_app') {
              sh 'venv/bin/python setup.py sdist bdist_wheel'
           }
       }
   }

   stage('SonarQube Analysis') {
        steps {
            dir('my_python_app') {
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: 'sonar_token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=my_python_app \
                        -Dsonar.sources=. \
                        -Dsonar.login=$SONAR_TOKEN \
                        '''
                    }
                }
           }
       }
          
    }

   stage('Quality Gate') {
       steps {
           waitForQualityGate abortPipeline: true
           sh 'echo "Quality Gate Passed!"'
       }
   }

   stage('Artifact Upload') {
       steps {
           dir('my_python_app') {
                sh '''
                jf rt upload dist/*.whl python-local/
                '''
           }
       }
   }

   stage('Docker Build') {
       steps {
            dir('my_python_app') {
                sh '''
                docker build -t python-fn-web-app:v1 .
                docker images | grep python-fn-web-app 
             ''' 
            }
       }
   }

   stage('Push Docker Image to JFrog Artifactory') {
       steps {
          withCredentials([usernamePassword(
              credentialsId: 'artifactory-credentials',
              usernameVariable: 'ARTIFACTORY_USERNAME',
              passwordVariable: 'ARTIFACTORY_PASSWORD'
          )]) {
              sh '''
              docker login artifactory.company.com \
              -u $ARTIFACTORY_USERNAME \
              -p $ARTIFACTORY_PASSWORD

              docker tag python-fn-web-app:v1 \
              artifactory.company.com/python-fn-web-app:v1

              docker push \
              artifactory.company.com/python-fn-web-app:v1
              '''
          }
       }
   }

   stage('Xray Security Scan') {
       steps {
           withCredentials([usernamePassword(
              credentialsId: 'artifactory-credentials',
              usernameVariable: 'ARTIFACTORY_USERNAME',
              passwordVariable: 'ARTIFACTORY_PASSWORD'
          )]) {
           sh '''
           curl -u $ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD -X POST "http://localhost:8081/artifactory/api/xray/scanArtifact" -H "Content-Type: application/json" -d '{
             "repoKey": "docker",
             "path": "artifactory.company.com/python-fn-web-app:v1"
           }'
           '''
       }
   }

   stage('Deploy to EC2') {
       steps {
           sshagent(credentials: ['ec2-key']) {
               sh '''
               scp -o StrictHostKeyChecking=no docker-compose.yml ec2-user@your_ec2_instance_ip:/home/ec2-user/
               ssh -o StrictHostKeyChecking=no ec2-user@your_ec2_instance_ip 'docker-compose -f /home/ec2-user/docker-compose.yml up -d'
               '''
           }
       }
   }
 
   stage('Health Check') {
            steps {
                sshagent(['ec2-key']) {
                    sh '''
                        sleep 15
                         
                        ssh -o StrictHostKeyChecking=no ubuntu@18.140.113.219 \
                        "curl -f http://localhost:8501"
                    '''
                }
            }
        }
    }
}
