---


---
# Azure Voting App - Test

## AKS

This Azure DevOps pipeline is designed for building, tesssting, and deploying applications to an Azure Kubernetes Service (AKS) cluster. It includes multiple stages for Continuous Integration (CI), Continuous Deployment (CD), and approval for both release and deployment processes.

### Pipeline Stages

1. **ApproveRelease_Build** :

* This stage is triggered manually and is used to approve the build process before continuing. It ensures that only approved builds are deployed.

1. **CI_Build** :

* The CI build stage handles the creation of a Docker image and pushes it to Azure Container Registry (ACR). It uses the Docker task for logging into the container registry and pushing the image.

1. **ApproveRelease_Deploy** :

* Like the build approval, this stage ensures that the deployment to AKS is manually approved before continuing. Once approved, the application will be deployed.

1. **CD_Deploy** :

* This stage performs the actual deployment to the AKS cluster. It updates the image tag in the Kubernetes manifest and then deploys it using the `KubernetesManifest@0` task, which is configured with the necessary Kubernetes service connection.

### Pipeline Variables

The pipeline uses several variables defined in `var.yml` for setting values related to the container registry, image repository, namespace, and other parameters.

```
variables:
  - name: containerRegistryServiceConnection
    value: votingapp
  - name: imageRepository
    value: crvoteapptestuks
  - name: containerRegistry
    value: crvoteapptestuks.azurecr.io
  - name: dockerfilePath
    value: '$(Build.SourcesDirectory)/azure-vote/Dockerfile'
  - name: tag
    value: '$(Build.BuildId)'
  - name: k8sNamespace
    value: votingapp
  - name: imagePullSecret
    value: crvoteapptestuks-auth
```

### Variables

The following variables are used for the deployment pipeline:

| Variable Name                          | Description                                                      | Example Value                                       |
| -------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------- |
| `containerRegistryServiceConnection` | Azure DevOps service connection name for the container registry. | `votingapp`                                       |
| `imageRepository`                    | Name of the container image repository.                          | `crvoteapptestuks`                                |
| `containerRegistry`                  | URL of the Azure Container Registry (ACR).                       | `crvoteapptestuks.azurecr.io`                     |
| `dockerfilePath`                     | Path to the Dockerfile used for building images.                 | `$(Build.SourcesDirectory)/azure-vote/Dockerfile` |
| `tag`                                | Build-specific tag for the container image.                      | `$(Build.BuildId)`                                |
| `k8sNamespace`                       | Kubernetes namespace for deployment.                             | `votingapp`                                       |
| `imagePullSecret`                    | Kubernetes secret for pulling images from ACR.                   | `crvoteapptestuks-auth`                           |

---

## Setting Up Service Connections

To enable deployment, a service connection to the Azure Container Registry (ACR) must be created in Azure DevOps. Follow these steps:

1. Navigate to your Azure DevOps project.
2. Go to **Project Settings** > **Service Connections**.
3. Click **New Service Connection** and select **Docker Registry**.
4. Fill in the details:
   - **Registry Type**: Azure Container Registry
   - **Azure Subscription**: Select your subscription
   - **Registry Name**: Select your container registry (`crvoteapptestuks`)
   - **Service Connection Name**: `votingapp` (as per the variable `containerRegistryServiceConnection`)
5. Save the connection.

---

## Creating a Variable Group in Azure DevOps

Variable groups allow you to manage and reuse variables across multiple pipelines. Follow these steps to create a variable group:

1. Navigate to your Azure DevOps project.
2. Go to **Pipelines** > **Library**.
3. Click **+ Variable Group**.
4. Name the group (e.g., `VotingAppVariables`) and add the following variables:
   | Variable Name                          | Value                                               |
   | -------------------------------------- | --------------------------------------------------- |
   | `containerRegistryServiceConnection` | `votingapp`                                       |
   | `imageRepository`                    | `crvoteapptestuks`                                |
   | `containerRegistry`                  | `crvoteapptestuks.azurecr.io`                     |
   | `dockerfilePath`                     | `$(Build.SourcesDirectory)/azure-vote/Dockerfile` |
   | `tag`                                | `$(Build.BuildId)`                                |
   | `k8sNamespace`                       | `votingapp`                                       |
   | `imagePullSecret`                    | `crvoteapptestuks-auth`                           |
5. Click **Save**.

---

## Kubernetes secret creation in cluster

- Ensure the Kubernetes secret `crvoteapptestuks-auth` is created in the namespace `votingapp` using the following command:
  ```bash
  kubectl create secret docker-registry crvoteapptestuks-auth \
    --docker-server=crvoteapptestuks.azurecr.io \
    --docker-username=<your-username> \
    --docker-password=<your-password> \
    --namespace=votingapp
  ```


### CI Build (`ci.yml`)

The `ci.yml` template is responsible for building the Docker image, pushing it to Azure Container Registry (ACR), and generating a CI version to be used later in the deployment process.

Steps include:

* Docker login to ACR
* Docker build and push tasks
* Generate a version identifier based on the build ID
* Publish the build artifacts

### CD Deployment (`cd.yml`)

The `cd.yml` template is responsible for deploying the application to the AKS cluster. It updates the Kubernetes manifest file to use the correct image tag and then deploys it using the `KubernetesManifest@0` task.

variables:

- name: containerRegistryServiceConnection
  value: votingapp
- name: imageRepository
  value: crvoteapptestuks
- name: containerRegistry
  value: crvoteapptestuks.azurecr.io
- name: dockerfilePath
  value: '$(Build.SourcesDirectory)/azure-vote/Dockerfile'
- name: tag
  value: '$(Build.BuildId)'
- name: k8sNamespace
  value: votingapp
- name: imagePullSecret
  value: crvoteapptestuks-auth

## Self-hosted Cluster Pipelines

This pipeline is designed for deploying applications to a Kubernetes cluster running on a Self-hosted infrastructure. It integrates with Azure DevOps to automate the deployment of containerized applications toSelf-hosted-managed Kubernetes clusters.

### Pipeline Stages

1. **ApproveRelease_Build** :

* Similar to the AKS pipeline, this stage requires manual approval before proceeding with the build process.

1. **CI_Build** :

* This stage builds the Docker image from the source code and pushes it to Azure Container Registry (ACR).

1. **ApproveRelease_Deploy** :

* This stage requires manual approval for deployment. It ensures that the release is fully approved before moving to deployment.

1. **CD_Deploy** :

* This stage deploys the application to theSelf-hosted Kubernetes cluster. It updates the Kubernetes manifest to include the correct image tag and then applies it using `kubectl`.

### Pipeline Variables

Similar to the AKS pipeline, this pipeline uses the `var.yml` file to define key variables for container registry, image repository, and other deployment parameters.

```
variables:
  - name: containerRegistryServiceConnection
    value: votingapp
  - name: imageRepository
    value: crvoteapptestuks
  - name: containerRegistry
    value: crvoteapptestuks.azurecr.io
  - name: dockerfilePath
    value: '$(Build.SourcesDirectory)/azure-vote/Dockerfile'
  - name: tag
    value: '$(Build.BuildId)'
  - name: k8sNamespace
    value: votingapp
  - name: imagePullSecret
    value: crvoteapptestuks-auth

```

### CI Build (`ci.yml`)

The CI build for Self-hosted is similar to the AKS pipeline but includes steps to ensure that the Docker image is correctly built and pushed to ACR. The manifest file is then updated with the new image tag, ensuring the correct version is deployed.

### CD Deployment (`cd.yml`)

In the `cd.yml` template for Self-hosted:

* The image tag in the manifest file is updated dynamically based on the build.
* The manifest is applied to the Self-hosted Kubernetes cluster using `kubectl`.
* The `KubernetesManifest@0` task is used to deploy the application to the Kubernetes cluster.

```kubectl
kubectl apply -f $(Build.SourcesDirectory)/azure-vote-all-in-one-redis.yaml --namespace $(k8sNamespace)

```

This pipeline automates the deployment of applications to Kubernetes clusters on Self-hosted infrastructure, similar to how the pipeline would work on AKS, ensuring efficient application delivery with manual approval steps for deployment and release stages.

## Reference links from Github repo
