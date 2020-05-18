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
These are instructions for importing this plugin into an existing airflow instance.  
To start, navigate to the root of your airflow workspace.

## Set up : Virtual environment

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

### Clone lumen into your plugins
`> git clone https://github.com/Raybeam/lumen_plugin plugins/lumen_plugin`

### Copy over Lumen requirements
`> cat plugins/lumen_plugin/requirements.txt >> requirements.txt`  
`> pip install requirements.txt`

### Set up Lumen
Move over the main Lumen DAG and sample DAGs (if wanted)

`> plugins/lumen_plugin/bin/lumen init`

`> plugins/lumen_plugin/bin/lumen add_samples`

Only the DAG works from the Lumen binary right now.

`> plugins/lumen_plugin/bin/lumen add_samples --dag_only`

### Disable rbac
In the root directory of your airflow workspace, open airflow.cfg and set `rbac=False`.

## Set up : Google Cloud Composer

### Create a Cloud Composer Environment
If you don't already have an existing Cloud Composer Environment, [create](https://console.cloud.google.com/composer/environments/create?_ga=2.148358327.1202999744.1589816907-593717271.1588273490) a Cloud Composer Environment.

### Install gcloud 
For macOS, run:  
`>brew cask install google-cloud-sdk`  
For Debian & Ubuntu, run:  
```
>echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
>curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
>sudo apt-get update && sudo apt-get install google-cloud-sdk
```

### Configure gcloud
Run `gcloud init` and follow the prompts to configure gcloud to connect to your Cloud Composer Environment.  
  
Enable cleaner CLI experience:  
`>gcloud config set accessibility/screen_reader true`

`>gcloud auth login`  
`>gcloud config set project <your Google Cloud project name>`  

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
