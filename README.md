# Lumen

<h1 align="center">
  <br>
  <img src="https://i.imgur.com/mAyZh0q.png" alt="Lumen">
  <br>
  Data confidence plugin for Airflow.
  <br>
  <br>
</h1>

The Lumen Airflow plugin makes it easy to communicate confidence about your data system to manager, executives and other stakeholders in your organization.  It improves trust in underlying data by increasing transparency.

# Lumen : Set up
These are instructions for importing this plugin into an existing airflow workspace.  
To start, navigate to the root of your airflow workspace.  
If you don't have an existing workspace, you can download the sample:  
```
>git clone https://github.com/Raybeam/lumen-test-airflow/ sample_workspace
>cd sample_workspace
```
  
The deployment environments are:  
[Local Deploy](#set-up--local-deploy)  
[Astronomer Deploy](#set-up--astronomer-deploy)  
[Google Cloud Composer Deploy](#set-up--google-cloud-composer-deploy)  

## Set up : Local Deploy

### Set up the Python virtual environment
`> python -m venv .`

### Set AIRFLOW_HOME
By putting the `AIRFLOW_HOME` env in the `bin/activate` file, you set the path each time you set up your venv.

`> echo "export AIRFLOW_HOME=$PWD" >> bin/activate`

### Activate your venv
`> source bin/activate`

### Install airflow
`> pip install apache-airflow`

### Initialize your Airflow DB
`> airflow initdb`

### Set up a user (admin:admin)
`> airflow create_user -r Admin -u admin -e admin@example.com -f admin -l user -p admin`

### Clone lumen into your plugins
`> git clone https://github.com/Raybeam/lumen_plugin plugins/lumen_plugin`

### Copy over Lumen requirements
`> cat plugins/lumen_plugin/requirements.txt >> requirements.txt`  
`> pip install -r requirements.txt`

### Set up Lumen
Move over the main Lumen DAG and sample DAGs (if wanted)

`> plugins/lumen_plugin/bin/lumen init`

`> plugins/lumen_plugin/bin/lumen add_samples`

Only the DAG works from the Lumen binary right now.

`> plugins/lumen_plugin/bin/lumen add_samples --dag_only`

### Enable rbac
In the root directory of your airflow workspace, open airflow.cfg and set `rbac=True`.

### Turn on Webserver
`>airflow webserver`

### Turn on Scheduler
In a new terminal, navigate to the same directory.  
`>source bin/activate`  
`>airflow scheduler`  

## Set up : Astronomer Deploy
### Set up local environment
Follow the local deploy [instructions](#set-up--local-deploy) for configuring your local environment.  

### Download Astronomer
Download astronomer package following their [tutorial](https://www.astronomer.io/docs/cli-getting-started/).

### Initialize Astronomer
In your working directory
`> astro dev init`

### Start Astronomer
`> astro dev start`
  
## Set up : Google Cloud Composer Deploy

### Clone lumen into your plugins
`> git clone https://github.com/Raybeam/lumen_plugin plugins/lumen_plugin`

### Install gcloud 
[Install](https://cloud.google.com/sdk/docs/quickstarts) the gcloud SDK and configure it to your Cloud Composer Environment.

### Updating requirements.txt in Google Cloud Composer (CLI)
`>gcloud auth login`  

`>gcloud config set project <your Google Cloud project name>`  

`>gcloud composer environments update  --update-pypi-packages-from-file=plugins/lumen_plugin/requirements.txt`

### Disable rbac
`>gcloud composer environments update --update-env-variables[rbac=False]`

### Uploading Plugin to Google Cloud Composer (CLI)
```
>gcloud composer environments storage plugins import\
    --environment ENVIRONMENT_NAME \
    --location LOCATION \
    --source SOURCE
```    

`ENVIRONMENT_NAME` is the name of the environment.  
`LOCATION` is the Compute Engine region where the environment is located.  
`SOURCE` is the absolute path to the local diretory/file to upload.  
