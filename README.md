# ML DevOps Dida Task

In this project, we deploy a simple text classification service based on a pre-trained NLP model.

## Getting Started

To set up your local development environment, please use a fresh virtual environment (`python -m venv .venv`), then run:

    pip install -r requirements.txt -r requirements-dev.txt
    pip install -e .

The first command will install all requirements for the application and to execute tests.
With the second command, you'll get an editable installation of the module, so that imports work properly.

You can now access the CLI with `python -m ml_devops_dida_task`.

Open `http://0.0.0.0:8000/docs` in FastAPI and test the prediction with new text.

To deploy this project as a docker container, please ensure that [Docker](https://docs.docker.com/install/) is installed.

### Testing

To execute the tests using test framework `pytest` , please run

    pytest tests

To run the tests with coverage information, please use

    pytest tests --cov=src --cov-report=html --cov-report=term

and have a look at the `htmlcov` folder, after the tests are done.

### Notebooks

To use your module code (`src/`) in Jupyter notebooks (`notebooks/`) without running into import errors, make sure to install the source locally

    pip install -e .

This way, you'll always use the latest version of your module code in your notebooks via `import ml_devops_dida_task`.

Assuming you already have Jupyter installed, you can make your virtual environment available as a separate kernel by running:

    pip install ipykernel

    python -m ipykernel install --user --name="ml-devops-dida-task"

Note that we mainly use notebooks for experiments, visualizations and reports. Every piece of functionality that is meant to be reused should go into module code and be imported into notebooks.

### Distribution Package

To build a distribution package (wheel), please use

    python setup.py bdist_wheel

You can find the build artifacts in the `dist` folder.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

    pip install -U pre-commit
    pre-commit install

If you run into any issues, you can remove the hooks again with `pre-commit uninstall`.

### How to run the application
- Step 1: When we push the code to the Github repository, Github Action will be triggered and the code will be updated in the repository and two Docker images (in DockerHub and Github Registry) with be created. See [GitHub Registry](https://github.com/JahedNaghipoor/ml-devops-dida-task/pkgs/container/ml-devops-dida-task) or [DockerHub](https://hub.docker.com/repository/docker/jahednaghipoor/ml_devops_dida_task/tags?page=1&ordering=last_updated)

- Step 2: To run the application in a scalable environment, we need to install Docker Desktop and K3d (lightweight Kubernetes for local users). To do that please proceed to [set up local environment](kubernetes_manifests/README.asciidoc)

- Step 3: Run Docker Desktop in your local machine and choose created k3d cluster as the current cluster in `kubeconfig` (if you already setup multiple Kubernetes cluster in your local system).

- Step 4: Run `sudo vi /private/etc/hosts` in mac or open `C:\Windows\System32\drivers\etc` as Admin mode in Windows and add the following command
  `127.0.0.1       dida-mlops.com`. This would let fast-api-dida.com to be opened in the browser. This step is needed as K3d does not have Ingress Controller by default. We dont need to do this step, when we use Kubernetes cloud version like EKS in AWS where we can take advantage of Route53.

- Step 5: Install mlflow as Helm chart:
   1. `helm repo add community-charts https://community-charts.github.io/helm-charts`
   2. `helm repo update`
   3. `helm install mlflow  community-charts/mlflow -n dida-mlops`
   4. `export POD_NAME=$(kubectl get pods -n dida-mlops -l "app.kubernetes.io/name=mlflow,app.kubernetes.io/instance=mlflow" -o jsonpath="{.items[0].metadata.name}")`
   5. `export CONTAINER_PORT=$(kubectl get pod -n dida-mlops $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")`
   6. `kubectl -n dida-mlops-test port-forward $POD_NAME 8080:$CONTAINER_PORT`

- Step 6: Run the following command to deploy necessary components for the application (deployment, service, ingress and hpa).
  
  `kubectl apply -f ./kubernetes_manifests`.
  
  That will deploy all necessary components to run the application in K3d.


### How to deploy the application in AWS

- Create an AWS account if you don't have any.
- Deploy code in AWS code commits.
- Use AWS CodeBuild for code deployment.
- Set up necessary IAM roles and permissions using Terraform.
- Provision Amazon EKS for Kubernetes.
- Store Docker images in Amazon ECR as container registery.
- Set up auto-scaling groups and configure scaling policies.
- Configure AWS Elastic Load Balancing or Kubernetes native features to distribute incoming traffic.
- Use AWS Route 53 for DNS management.

## Contact

Dr. Jahed Naghipoor (jahednaghipoor1361@gmail.com)

## License

© Dr. Jahed Naghipoor
