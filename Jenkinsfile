node('docker-builder') {

    stage('Checkout') {
        checkout scm
    }

    stage('Build flask') {
        dockerImage = buildDockerfile "hcx-quickbooks-dashboard-flask", "Dockerfile"
    }

    stage('Build nginx'){
        buildDockerfile "hcx-quickbooks-dashboard-nginx", "Dockerfile.nginx"
    }

    stage('Run tests'){
        withPostgresServer {
            dockerImage.inside {
                    sh 'alembic upgrade head'
                    sh 'alembic downgrade base'
                    sh 'alembic upgrade head'
                }
            withEnv(['HCG_UTILS_AUTHENTICATION_JWT_VERIFY=no']){
               pytest(dockerImage)
            }      
        }
    }
    

    stage('SonarQube analysis') {
        sonarScan 'hcx-quickbooks-dashboard'
    }

    stage('Helm chart'){
        helmLint 'charts'
        inMaster{
            helmPublish 'charts/hcx-quickbooks-dashboard'
        }
    }

    inMaster {
        stage('Migrate') {
            def alembic = dockerImage
            applyAlembicMigration(dockerImage,alembic)
        }
    }
}

stage("Quality Gate"){
    sonarQualityGate()
}