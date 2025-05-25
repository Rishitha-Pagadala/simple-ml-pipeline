pipeline {
    agent any // Specifies that Jenkins can run this pipeline on any available agent/node

    environment {
        IMAGE_NAME = 'simple-ml-app-jenkins'
        HOST_MODEL_OUTPUT_DIR = 'jenkins_model_output'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out code from Git...'
                checkout scm
            }
        }

        stage('2. Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}..."
                // Use bat for Windows command prompt
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('3. Train Model (Run Docker Container)') {
            steps {
                echo "Training model and saving to ${HOST_MODEL_OUTPUT_DIR}..."

                // Use bat for Windows mkdir. %WORKSPACE% for environment variables in bat.
                // Quotes around paths are good practice if they might contain spaces.
                bat "if not exist \"%WORKSPACE%\\${HOST_MODEL_OUTPUT_DIR}\" mkdir \"%WORKSPACE%\\${HOST_MODEL_OUTPUT_DIR}\""

                // Use bat for docker run.
                bat """
                    docker run --rm ^
                        -v "%WORKSPACE%\\${HOST_MODEL_OUTPUT_DIR}:/app/model" ^
                        ${IMAGE_NAME}
                """
                // Note: In bat, the line continuation character is '^', not '\'.
                // However, Jenkins 'bat' step with triple quotes often handles multi-line commands well
                // even with '\' if the underlying command (docker) supports it. Let's try with '^' for clarity.
                // If docker run itself needs '\', it might still work due to how Jenkins passes it.
            }
        }

        stage('4. Verify Model Output') {
            steps {
                echo "Verifying model output in Jenkins workspace at %WORKSPACE%\\${HOST_MODEL_OUTPUT_DIR}..."
                // Use bat for Windows dir command
                bat "dir \"%WORKSPACE%\\${HOST_MODEL_OUTPUT_DIR}\""

                // Use bat for Windows file existence check
                // If the file exists, the 'if exist' is true. If not, it's false.
                // We'll set an errorlevel if it doesn't exist to fail the step.
                bat """
                    if exist "%WORKSPACE%\\${HOST_MODEL_OUTPUT_DIR}\\iris_model.joblib" (
                        echo SUCCESS: Model file iris_model.joblib found!
                    ) else (
                        echo ERROR: Model file iris_model.joblib not found!
                        exit /b 1
                    )
                """
                // 'exit /b 1' sets an errorlevel that Jenkins pipeline should recognize as failure for the 'bat' step.
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            // Example for cleaning up with bat, if needed later:
            // bat "docker rmi ${IMAGE_NAME} || echo Image not found or in use"
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}