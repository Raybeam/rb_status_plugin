#!/bin/bash

################################################################################
# help                                                                         #
################################################################################
help()
{
   # Display help
   echo "This script will deploy the rb Status plugin to an environment, using the instructions listed in the README.md file."
   echo
   echo
   echo "Required parameters:"
   echo "environment               The environment you'd like to deploy to."
   echo "                          (local, astronomer_local, astronomer_remote, google_cloud_composer)"
   echo
   echo
   echo
   echo "Example:"
   echo -e "\t./plugins/rb_status_plugin/deploy.sh --environment=local"
   echo
}

################################################################################
# Prompt for local deploy, whether to include samples                          #
################################################################################
prompt_local_install_type()
{
  while true; do
    echo -e "\n\nPlease select which type of deployment you would like:\n\t[1]\tbasic plugin install\n\t[2]\tplugin install and sample dags\n\t[3]\tplugin install and all samples"
    read user_input_environment 
    echo
    case $user_input_environment in
      "1"|"basic plugin install")
        echo -e "\nInstalling plugin...\n"
        plugins/rb_status_plugin/bin/rb_status init
        break
        ;;
      "2"|"plugin install and sample dags")
        echo -e "\nInstalling plugin with sample dags...\n"
        plugins/rb_status_plugin/bin/rb_status init
        plugins/rb_status_plugin/bin/rb_status add_samples --dag_only
        break
        ;;
      "3"|"plugin install and all samples")
        echo -e "\nInstalling plugin with all samples...\n"
        plugins/rb_status_plugin/bin/rb_status init
        plugins/rb_status_plugin/bin/rb_status add_samples
        break
        ;;
      "4"|"google_cloud_composer")
        echo -e "\nEnvironment set to: google_cloud_composer\n"
        environment="google_cloud_composer"
        break
        ;;
      *)
        echo -e "\nInvalid choice...\n"
    esac
  done
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

  echo -e "\n\n\nInstalling required python packages..."
  echo >> requirements.txt
  cat plugins/rb_status_plugin/requirements.txt >> requirements.txt
  sort -u requirements.txt  > requirements2.txt
  mv requirements2.txt requirements.txt 
  pip3 install -r requirements.txt

  echo -e "\n\n\nInstalling and configuring airflow in virtual environment..."
  pip3 install apache-airflow
  pip3 install psycopg2
  airflow initdb
  airflow create_user -r Admin -u admin -e admin@example.com -f admin -l user -p admin

  echo -e "\n\nInstalling rb_status_plugin..."
  prompt_local_install_type
}

################################################################################
# List choices and parse answer for prompt                                     #
################################################################################
format_prompt() {
  config_param="$1"
  shift
  local list_choices=("$@")

  for i in "${!list_choices[@]}"; do 
    printf "%s\t%s\n" "[$i]" "${list_choices[$i]}"
  done
  read choice_selected

  if [[ " ${list_choices[@]} " =~ " $choice_selected " ]]; then
    echo -e "$config_param set to $choice_selected"
    prompt_in_progress=false
  else
    case $choice_selected in
    ''|*[!0-9]*)
      echo -e "$choice_selected is an invalid choice."
      ;;
    *)
      if [ $(($choice_selected < ${#list_choices[@]})) ]; then
        choice_selected="${list_choices[$choice_selected]}"
        echo -e "$config_param set to $choice_selected"
        prompt_in_progress=false
      else
        echo -e "$choice_selected is an invalid choice."
      fi
      ;;
    esac
  fi
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


  prompt_in_progress=true
  while $prompt_in_progress; do
    echo -e "\n\n\n"
    echo "Please select one of the following regions to deploy to:"
    region_list=( $(gcloud compute regions list --format="value(name)") )
    format_prompt "region" "${region_list[@]}"
  done
  LOCATION=$choice_selected


  prompt_in_progress=true
  while $prompt_in_progress; do
    echo -e "\n\n\n"
    project_list=( $(gcloud projects list --format="value(name)") )
    echo "Please select one of the following projects:"
    format_prompt "project" "${project_list[@]}"
  done
  PROJECT_NAME=$choice_selected

  prompt_in_progress=true
  while $prompt_in_progress; do
    echo -e "\n\n\n"
    environment_list=( $(gcloud composer environments list --locations $LOCATION  --format="value(name)") )
    echo "Please select one of the following environments:"
    format_prompt "environment" "${environment_list[@]}"
  done
  ENVIRONMENT_NAME=$choice_selected


  gcloud config set project $PROJECT_NAME
  echo "updating requirements..."
  cat $(pwd)/plugins/rb_status_plugin/requirements.txt | while read requirement 
  do
    echo -e "installing python package: $requirement.."
    gcloud beta composer environments update $ENVIRONMENT_NAME --location $LOCATION --update-pypi-package=$requirement
  done
  echo -e "\n\nsetting airflow configurations..."
  gcloud composer environments update $ENVIRONMENT_NAME --location $LOCATION --update-airflow-configs webserver-rbac=False,core-store_serialized_dags=False,webserver-async_dagbag_loader=True,webserver-collect_dags_interval=10,webserver-dagbag_sync_interval=10,webserver-worker_refresh_interval=3600
  echo -e "\n\ninstalling rb-status plugin..."
  gcloud composer environments storage dags import --environment=$ENVIRONMENT_NAME --location $LOCATION --source $(pwd)/plugins/rb_status_plugin/setup/rb_status.py
  gcloud composer environments storage plugins import --environment=$ENVIRONMENT_NAME --location $LOCATION --source $(pwd)/plugins/rb_status_plugin/
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
    echo -e "\n\nTo start airflow webserver, please open a new tab and run:\n\tcd '$(pwd)'; source \"bin/activate\"; airflow webserver"
    echo -e "\n\nTo start airflow scheduler, please open a new tab and run:\n\tcd '$(pwd)'; source \"bin/activate\"; airflow scheduler"
}

################################################################################
#  Prompt user asking where they wish to deploy.                               #
################################################################################
prompt_deploy()
{
  while true; do
    echo -e "\n\nEnvironment not specified. Please select one of the following choices:\n\t[1]\tlocal\n\t[2]\tastronomer_local\n\t[3]\tastronomer_remote\n\t[4]\tgoogle_cloud_composer"
    read user_input_environment 
    echo
    case $user_input_environment in
      "1"|"local")
        echo -e "\nEnvironment set to: local\n"
        environment="local"
        break
        ;;
      "2"|"astronomer_local")
        echo -e "\nEnvironment set to: astronomer_local\n"
        environment="astronomer_local"
        break
        ;;
      "3"|"astronomer_remote")
        echo -e "\nEnvironment set to: astronomer_remote\n"
        environment="astronomer_remote"
        break
        ;;
      "4"|"google_cloud_composer")
        echo -e "\nEnvironment set to: google_cloud_composer\n"
        environment="google_cloud_composer"
        break
        ;;
      *)
        echo -e "\nInvalid choice...\n"
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
  echo -e "Directory '$(pwd)' is not empty. Running this script may overwrite files in the directory.\nAre you sure you want to do this?(Y/n)"
  read boolean_run_script
  echo
  case $boolean_run_script in
    [yY])
      echo -e "\n\nStarting deploy script..."
      deploy_plugin
      ;;
    *)
      echo -e "\n\nExiting deploy script..."
      exit 1
  esac
else
  echo -e "\n\nStarting deploy script..."
  exit 1
  deploy_plugin
fi