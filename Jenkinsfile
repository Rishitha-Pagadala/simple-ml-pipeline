pipeline {
    agent any // Specifies that Jenkins can run this pipeline on any available agent/node

    environment {
        // Define an environment variable for the image name
        IMAGE_NAME = 'simple-ml-app-jenkins'
        // Define the host output directory relative to Jenkins workspace
        // Jenkins will create a 'workspace' for each job run.
        // We'll create our model output directory inside this workspace.
        HOST_MODEL_OUTPUT_DIR = 'jenkins_model_output'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out code from Git...'
                // 'scm' is a special variable that refers to the Source Code Management
                // configuration of the Jenkins job (which we will set up to point to your GitHub repo).
                checkout scm
            }
        }

        stage('2. Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}..."
                // 'sh' executes a shell command.
                // On Windows, if Jenkins is running directly (not in WSL/Linux container),
                // you might use 'bat' for .bat scripts or 'powershell' for PowerShell scripts.
                // However, 'docker' commands are usually accessible via 'sh' if Git Bash tools are in PATH
                // or if Docker Desktop configured PATH correctly. Let's try with 'sh' first.
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('3. Train Model (Run Docker Container)') {
            steps {
                echo "Training model and saving to ${HOST_MODEL_OUTPUT_DIR}..."

                // Ensure the host output directory exists in the Jenkins workspace.
                // ${WORKSPACE} is a built-in Jenkins environment variable that points to
                // the absolute path of the current job's workspace.
                sh "mkdir -p ${WORKSPACE}/${HOST_MODEL_OUTPUT_DIR}"

                // Run the Docker container, mounting the Jenkins workspace output dir.
                // The '"""' (triple double quotes) allow for a multi-line shell command.
                sh """
                    docker run --rm \
                        -v ${WORKSPACE}/${HOST_MODEL_OUTPUT_DIR}:/app/model \
                        ${IMAGE_NAME}
                """
                // The train.py script inside the container will save the model to /app/model,
                // which is mapped to ${WORKSPACE}/${HOST_MODEL_OUTPUT_DIR} on the Jenkins agent (your machine).
            }
        }

        stage('4. Verify Model Output') {
            steps {
                echo "Verifying model output in Jenkins workspace at ${WORKSPACE}/${HOST_MODEL_OUTPUT_DIR}..."
                // List the contents of the output directory
                sh "ls -l ${WORKSPACE}/${HOST_MODEL_OUTPUT_DIR}"

                // Basic check: Test if the model file exists.
                // 'test -f' checks if a file exists and is a regular file.
                // The '&& echo ...' part only runs if the 'test -f' command is successful (exit code 0).
                sh "test -f ${WORKSPACE}/${HOST_MODEL_OUTPUT_DIR}/iris_model.joblib && echo 'SUCCESS: Model file iris_model.joblib found!'"
            }
        }
    }

    post {
        // The 'post' section defines actions to be taken after the stages complete.
        always {
            // This block runs regardless of whether the pipeline succeeded or failed.
            echo 'Pipeline finished.'
            // Optional: Clean up the Docker image built by this specific pipeline run.
            // Using "|| true" ensures that if the 'docker rmi' command fails (e.g., image not found, or in use by another container),
            // it doesn't cause the entire 'post' section or pipeline to be marked as failed.
            // sh "docker rmi ${IMAGE_NAME} || true" // Commented out for now, can be enabled later.
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}