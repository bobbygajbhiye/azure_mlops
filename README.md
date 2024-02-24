<br />
<div align="center">
  <h1 align="center">Azure MLOps CI/CD Pipeline Implementation</h1>
</div>

This repository is dedicated to sharing insights and challenges faced in implementing an MLOps CI/CD pipeline using Azure. From training a simple machine learning model to deploying it production-ready using Azure MLOps principles, the journey entails numerous steps, each with its own set of challenges. This documentation aims to serve as a detailed guide, shedding light on each step involved in the pipeline and the issues faced during implementation.

<br />
<div align="center">
  <h2 align="center">Getting Started</h1>
</div>
Deploying machine learning models to production can be complex and fraught with challenges. Recognizing the scarcity of detailed, step-by-step guides, this repository offers comprehensive insights into each process step. Below, you'll find a summary of the steps I followed, accompanied by short descriptions to provide context and guidance.

1. Get Free Trial Azure Subscription<br />
Start by signing up for a free trial Azure subscription to access Azure services. It's an essential first step to utilize Microsoft's cloud resources for deploying machine learning models.

2. Create Resource Group Manually<br />
A resource group is a container that holds related resources for an Azure solution. Creating a resource group manually is necessary for organizing the resources you'll need for the MLOps pipeline.

3. Register for Essential Resource Providers
Navigate to Subscriptions on the Azure portal, open Resource providers, and register for Storage, KeyVault, MachineLearningServices, and Insights. These services are critical for storing data, managing secrets, executing machine learning services, and monitoring.

4. Create Project in DevOps
Setting up a project in Azure DevOps is vital for managing the repository, pipelines, and tasks associated with your MLOps project.

5. Create Service Connection
Establish a service connection in Azure DevOps. This facilitates secure communication and integration between Azure DevOps and Azure resources.

6. Clone Repo in GitHub
Clone the repository in GitHub to start version controlling your code and pipeline configurations.

7. Import Pipeline Using YML File
Import the pipeline configuration using the YAML file in the repository. YAML files describe the CI/CD process in Azure Pipelines.

8. Create Variables Group
Create a variables group in Azure DevOps to manage and organize variables used across pipelines, enhancing maintainability and scalability.

9. Give Variables Group Access Permission to Pipeline
Configuring access permissions ensures that your pipeline can securely access and utilize the variables defined in the variables group.

10. Create Agent
Create an agent in Azure Pipelines. Agents run build and deployment jobs in your DevOps CI/CD pipelines.

11. Run the Pipeline and Check Created Artifacts
Trigger the pipeline run to check the creation of artifacts. Artifacts are the outputs of the build process, serving as deployment units.

12. Enable Release Pipelines from Pipeline Settings
Enable release pipelines in Azure Pipelines settings to manage deployment stages and environments efficiently.

13. Create New Release Pipeline and Stage
Set up a new release pipeline and configure its stages. This defines the sequence and condition under which your model is deployed across different environments.

14. Change Agent Job Name and Pool in Release Pipeline
Adjust the agent job name and switch the agent pool to default in the release pipeline settings. This ensures the proper execution environment for deployment tasks.

15. Create Variables Group for Release Pipeline
Similar to step 8, create a variables group specifically for the release pipeline to manage deployment-related variables effectively.

16. Link Variables Groups to Release Pipeline
Linking variables groups to the release pipeline grants it access to necessary configurations, fostering a smooth deployment process.

17. Run Release Pipeline
Finally, run the release pipeline to deploy the machine learning model to the production environment. Monitor the process and verify successful deployment.

This guide aims to demystify the process of deploying machine learning models using Azure MLOps CI/CD pipeline, making it accessible and understandable. Contributions and discussions are welcome to enhance this guide further. Happy coding and deploying!
