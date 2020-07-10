# Raybeam Status Plugin 

<h1 align="center">
  <br>
  <img src="https://i.imgur.com/mAyZh0q.png" alt="Raybeam Status Plugin">
  <br>
  Data confidence plugin for Airflow.
  <br>
  <br>
</h1>

The Status Airflow plugin makes it easy to communicate confidence about your data system to manager, executives and other stakeholders in your organization.  It improves trust in underlying data by increasing transparency.

# Set up
These are instructions for importing this plugin into an existing airflow workspace.  
To start, navigate to the root of your airflow workspace.  
If you don't have an existing workspace, you can download the sample:  
```
>git clone https://github.com/Raybeam/rb_test_airflow/ sample_workspace
>cd sample_workspace
```
  
The deployment environments are:  
[Local Deploy](#set-up--local-deploy)  
[Astronomer Deploy](#set-up--astronomer-deploy)  
[Google Cloud Composer Deploy](#set-up--google-cloud-composer-deploy)  

## Quick Setup
Clone a sample airflow workspace (if you dont have an existing airflow repository).  
```
git clone https://github.com/Raybeam/rb_test_airflow/ sample_workspace
cd sample_workspace
```

Clone deploy script into local workspace  
```
git clone https://github.com/Raybeam/rb_plugin_deploy plugins/rb_plugin_deploy
```  
  
Run deploy script.  
```
./plugins/rb_plugin_deploy/deploy.sh
```
  
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

### Clone the status plugin into your plugins
`> git clone https://github.com/Raybeam/rb_status_plugin plugins/rb_status_plugin`

### Copy over rb status requirements
`> cat plugins/rb_status_plugin/requirements.txt >> requirements.txt`  
`> pip install -r requirements.txt`

### Set up rb status
Move over the main rb status DAG and sample DAGs (if wanted)

`> plugins/rb_status_plugin/bin/rb_status init`

`> plugins/rb_status_plugin/bin/rb_status add_samples`

Only the DAG works from the rb status plugin binary right now.

`> plugins/rb_status_plugin/bin/rb_status add_samples --dag_only`

### Enable rbac
In the root directory of your airflow workspace, open airflow.cfg and set `rbac=True`.

### Turn on Webserver
`>airflow webserver`

### Turn on Scheduler
In a new terminal, navigate to the same directory.  
`>source bin/activate`  
`>airflow scheduler`  

### Interact with UI
In a web brower, visit localhost:8080.  
If you see a tab for "Status" in the header, then the installation was a success.

## Set up : Astronomer Deploy
### Set up local environment
Follow the local deploy [instructions](#set-up--local-deploy) for configuring your local environment.  

### Turn off Webserver and Scheduler
Either Control+C or closing the terminal's window/tab should work to turn either of them off. 

### Download Astronomer
Download astronomer package following their [tutorial](https://www.astronomer.io/docs/cli-getting-started/).

### Initialize Astronomer
In your working directory
`> astro dev init`

### Start Astronomer
`> astro dev start`
  
### Interact with UI
In a web brower, visit localhost:8080.  
If you see a tab for "Status" in the header, then the installation was a success.

## Set up : Google Cloud Composer Deploy

### Clone the status plugin into your plugins
`> git clone https://github.com/Raybeam/rb_status_plugin plugins/rb_status_plugin`

### Install gcloud 
[Install](https://cloud.google.com/sdk/docs/quickstarts) the gcloud SDK and configure it to your Cloud Composer Environment.

### Updating requirements.txt in Google Cloud Composer (CLI)
`>gcloud auth login`  

`>gcloud config set project <your Google Cloud project name>`  

`>gcloud composer environments update ENVIRONMENT_NAME --location LOCATION --update-pypi-packages-from-file=plugins/rb_status_plugin/requirements.txt`  

`ENVIRONMENT_NAME` is the name of the environment.  
`LOCATION` is the Compute Engine region where the environment is located.  
It may take a few minutes for cloud composer to finish updating after running this command.

### Import Required Airflow Configurations
```
>gcloud composer environments update ENVIRONMENT_NAME --location LOCATION --update-airflow-configs \  
	webserver-rbac=False,\  
	core-store_serialized_dags=False,\  
	webserver-async_dagbag_loader=True,\  
	webserver-collect_dags_interval=10,\  
	webserver-dagbag_sync_interval=10,\  
	webserver-worker_refresh_interval=3600
```  

`ENVIRONMENT_NAME` is the name of the environment.  
`LOCATION` is the Compute Engine region where the environment is located.  


### Uploading Plugin to Google Cloud Composer (CLI)
Add rb_status dag to dags folder:  
```
 >gcloud composer environments storage dags import\  
    --environment ENVIRONMENT_NAME \
    --location LOCATION \
    --source SOURCE/setup/rb_status.py
```  

Add rb_status plugin to plugins folder:  
```
>gcloud composer environments storage plugins import\
    --environment ENVIRONMENT_NAME \
    --location LOCATION \
    --source SOURCE
```    

`ENVIRONMENT_NAME` is the name of the environment.  
`LOCATION` is the Compute Engine region where the environment is located.  
`SOURCE` is the absolute path to the local directory (full-path/plugins/rb_status_plugin/).  
