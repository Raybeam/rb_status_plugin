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
   echo "environment               The environment you'd like to deploy to. (local, astronomer, google_cloud_composer)"
   echo "install_dependencies      Whether to install all required depencies (True, False)"
   echo "operating_system          The OS on which the script is being run (macOS, Ubuntu)"
   echo
   echo
   echo
   echo "Example:"
   echo -e "\t./plugins/lumen_plugin/deploy.sh --environment=local --operating_system=macOS --install_dependencies=True"
   echo
}

################################################################################
# Deploy Locally                                                               #
################################################################################
deploy_local()
{
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
  git clone https://github.com/Raybeam/lumen_plugin plugins/lumen_plugin
  echo >> requirements.txt
  cat plugins/lumen_plugin/requirements.txt >> requirements.txt
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
  python3 -m venv .
  source "bin/activate"
  git clone https://github.com/Raybeam/lumen_plugin plugins/lumen_plugin
  if [ "$operating_system" == "Ubuntu" ]; then
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
    sudo apt-get update && sudo apt-get install google-cloud-sdk
  else
    brew cask install gcloud
  fi

  gcloud init
  gcloud config set accessibility/screen_reader true
  gcloud auth login

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
# Deploy to Astronomer                                                         #
################################################################################
deploy_astronomer()
{
  echo "Not implemented yet..."
}

################################################################################
# Deploy plugin (based on environment chosen)                                  #
################################################################################
deploy_plugin()
{
  if [ "$environment" == "local" ]; then
    deploy_local
    start_airflow
  elif [ "$environment" == "google_cloud_composer" ]; then
    deploy_gcc
  elif [ "$environment" == "astronomer" ]; then
    deploy_astronomer
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
  if [ "$operating_system" == "Ubuntu" ]; then
    x-terminal-emulator --window-with-profile="$(id -u)" --working-directory=$(pwd) -e "echo \"Starting webserver...\";. \"bin/activate\"; airflow webserver"
    x-terminal-emulator --window-with-profile="$(id -u)" --working-directory=$(pwd) -e "echo \"Starting scheduler...\";. \"bin/activate\"; airflow scheduler"
  else
    osascript -e 'tell application "Terminal"
       do script "echo \"Starting webserver...\";cd '$(pwd)'; source \"bin/activate\"; airflow webserver"
    end tell'
    osascript -e 'tell application "Terminal"
       do script "echo \"Starting scheduler...\";cd '$(pwd)'; source \"bin/activate\"; airflow scheduler"
    end tell'
  fi
}


################################################################################
#  Main Code.                                                                  #
################################################################################
while [ $# -gt 0 ]; do
  case "$1" in
    --help)
      help
      exit;;
    --environment=*)
      environment="${1#*=}"
      ;;
    --install_dependencies=*)
      install_dependencies="${1#*=}"
      ;;
    --operating_system=*)
      operating_system="${1#*=}"
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
if [ -z ${operating_system+x} ]; then
  operating_system="macOS"
fi
if [ -z ${install_dependencies+x} ]; then
  install_dependencies="True"
fi

printf "environment is set to:                 %s\n" "$environment"
printf "operating_system is set to:            %s\n" "$operating_system"
printf "install_dependencies is set to:        %s\n" "$install_dependencies"

deploy_plugin