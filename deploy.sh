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
  sort -u requirements.txt | tee requirements.txt 
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
  gcloud composer environments update $ENVIRONMENT_NAME --location $LOCATION --update-pypi-packages-from-file=plugins/lumen_plugin/requirements.txt
  gcloud composer environments update $ENVIRONMENT_NAME --location $LOCATION --update-env-variables rbac=False
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
   echo -e "To start astro-airflow instance, please run:\n\tsudo astro dev start"
  else
    echo -e "To start astro-airflow instance, please run:\n\tastro dev start"
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
    sudo astro dev deploy
  else
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
  environment="local"
fi

deploy_plugin