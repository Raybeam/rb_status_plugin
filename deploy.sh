#!/bin/bash

################################################################################
# help                                                                         #
################################################################################
help()
{
   # Display help
   echo "This script will deploy the lumen plugin to an environment, using the instructions listed in the README.md file."
   echo
   echo
   echo "Required parameters:"
   echo "environment               The environment you'd like to deploy to."
   echo "                          (local, astronomer_local, astronomer_remote, google_cloud_composer)"
   echo
   echo
   echo
   echo "Example:"
   echo -e "\t./plugins/lumen_plugin/deploy.sh --environment=local"
   echo
}

################################################################################
# Deploy Locally                                                               #
################################################################################
deploy_local()
{
  declare -a dependencies=("python3" "pip3" "git")
  for val in $dependencies; do
      if ! [ -x "$(command -v $val)" ]; then
        printf "Unable to complete deploy, please install %s\n" "$val."
        exit 1
      fi
  done
  echo "Deploying airflow locally..."
  echo -e "\n\n\nCreating virtual environment..."
  python3 -m venv .
  source "bin/activate"
  echo "export AIRFLOW_HOME=$PWD" >> bin/activate

  echo -e "\n\n\nInstalling and configuring airflow in virtual environment..."
  pip3 install apache-airflow
  pip3 install psycopg2
  airflow initdb
  airflow create_user -r Admin -u admin -e admin@example.com -f admin -l user -p admin

  echo >> requirements.txt
  cat plugins/lumen_plugin/requirements.txt >> requirements.txt
  sort -u requirements.txt  > requirements2.txt
  mv requirements2.txt requirements.txt 
  pip3 install -r requirements.txt

  plugins/lumen_plugin/bin/lumen init
  plugins/lumen_plugin/bin/lumen add_samples
  plugins/lumen_plugin/bin/lumen add_samples --dag_only
}

################################################################################
# Deploy to Google Cloud Composer                                              #
################################################################################
deploy_gcc()
{
  if ! [ -x "$(command -v gcloud)" ]; then
    echo "Unable to complete deploy, please install gcloud."
    exit 1
  fi

  echo -e "\n\n\n"
  echo "Please enter the location of the environment (ie. us-west3):"
  read LOCATION

  echo -e "\n\n\n"
  gcloud projects list
  echo "Please enter the name of the project:"
  read PROJECT_NAME

  echo -e "\n\n\n"
  gcloud composer environments list --locations $LOCATION
  echo "Please enter the name of the environment:"
  read ENVIRONMENT_NAME

  gcloud config set project $PROJECT_NAME
  echo "updating requirements..."
  cat $(pwd)/plugins/lumen_plugin/requirements.txt | while read requirement 
  do
    echo -e "installing python package: $requirement.."
    gcloud beta composer environments update $ENVIRONMENT_NAME --location $LOCATION --update-pypi-package=$requirement
  done
  echo -e "\n\nsetting airflow configurations..."
  gcloud composer environments update $ENVIRONMENT_NAME --location $LOCATION --update-airflow-configs webserver-rbac=False,core-store_serialized_dags=False,webserver-async_dagbag_loader=True,webserver-collect_dags_interval=10,webserver-dagbag_sync_interval=10,webserver-worker_refresh_interval=3600
  echo -e "\n\ninstalling rb-status plugin..."
  gcloud composer environments storage dags import --environment=$ENVIRONMENT_NAME --location $LOCATION --source $(pwd)/plugins/lumen_plugin/setup/lumen.py
  gcloud composer environments storage plugins import --environment=$ENVIRONMENT_NAME --location $LOCATION --source $(pwd)/plugins/lumen_plugin/
}

################################################################################
# Deploy to Astronomer Locally                                                 #
################################################################################
deploy_astronomer_local()
{
  if ! [ -x "$(command -v astro)" ]; then
    echo "Unable to complete deploy, please install astro."
    exit 1
  fi
  
  deploy_local

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
   echo -e "To start astro-airflow instance, please run:\n\tsudo astro dev init\n\tsudo astro dev start"
  else
    echo -e "To start astro-airflow instance, please run:\n\tastro dev init\n\tastro dev start"
  fi
}
################################################################################
# Deploy to Astronomer Remotely                                                #
################################################################################
deploy_astronomer_remote()
{
  if ! [ -x "$(command -v astro)" ]; then
    echo "Unable to complete deploy, please install astro."
    exit 1
  fi

  deploy_local

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo astro dev init
    sudo astro dev deploy
  else
    astro dev init
    astro dev deploy
  fi
}

################################################################################
# Deploy plugin (based on environment chosen)                                  #
################################################################################
deploy_plugin()
{
  if [ "$environment" == "local" ]; then
    deploy_local
    start_airflow
  elif [ "$environment" == "astronomer_local" ]; then
    deploy_astronomer_local
  elif [ "$environment" == "astronomer_remote" ]; then
    deploy_astronomer_remote
  elif [ "$environment" == "google_cloud_composer" ]; then
    deploy_gcc
  else
    echo "Error: Environment not specified."
    help
  fi
}

################################################################################
# Start Webserver and Scheduler                                                #
################################################################################
start_airflow()
{
    echo -e "\n\n\n\nTo start airflow webserver, please open a new tab and run:\n\tcd '$(pwd)'; source \"bin/activate\"; airflow webserver"
    echo -e "\n\nTo start airflow scheduler, please open a new tab and run:\n\tcd '$(pwd)'; source \"bin/activate\"; airflow scheduler"
}

################################################################################
#  Prompt user asking where they wish to deploy.                               #
################################################################################
prompt_deploy() {
    while true; do
      echo -e "Environment not specified. Please select one of the following choices:\n\t[1] local\n\t[2]astronomer_local\n\t[3]astronomer_remote\n\t[4]google_cloud_composer\n\n"
      read user_input_environment 
      echo
      case $user_input_environment in
        "1"|"local")
          echo "Environment set to: local"
          environment="local"
          break
          ;;
        "2"|"astronomer_local")
          echo "Environment set to: astronomer_local"
          environment="astronomer_local"
          break
          ;;
        "3"|"astronomer_remote")
          echo "Environment set to: astronomer_remote"
          environment="astronomer_remote"
          break
          ;;
        "4"|"google_cloud_composer")
          echo "Environment set to: google_cloud_composer"
          environment="google_cloud_composer"
          break
          ;;
        *)
          echo -e "Invalid choice...\n\n"
      esac
    done
}

################################################################################
#  Main Code.                                                                  #
################################################################################
while [ $# -gt 0 ]; do
  case "$1" in
    --help)
      help
      exit 1;;
    --environment=*)
      environment="${1#*=}"
      ;;
    *)
      printf "**********************************************************************************\n"
      printf "Error: Invalid argument. \""
      printf $1
      printf "\" is not defined.\n"
      printf "**********************************************************************************\n\n\n"
      help
      exit 1
  esac
  shift
done

if [ -z ${environment+x} ]; then
  prompt_deploy
fi

if [ "$(ls -A $(pwd))" ]; then
  echo -e "Directory '$(pwd)' is not empty. Running this script may overwrite files in the directory.\n\nAre you sure you want to do this?(Y/n)"
  read boolean_run_script
  echo
  case $boolean_run_script in
    [yY])
      echo "Starting depoloy script..."
      deploy_plugin
      ;;
    *)
      echo "Exiting deploy script..."
      exit 1
  esac
else
  echo "Starting depoloy script..."
  exit 1
  deploy_plugin
fi