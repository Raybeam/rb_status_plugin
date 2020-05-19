#!/bin/bash
################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "This script will deploy the lumen plugin to an environment, using the instructions listed in the README.md file."
   echo
   echo
   echo "Required parameters:"
   echo "environment               The environment you'd like to deploy to. (local, astronomer, google_cloud_composer)"
   echo "install_dependencies      Whether to install all required depencies (True, False)"
   echo "operating_system          The OS on which the script is being run (macOS, Ubuntu, Windows)"
   echo
   echo
   echo 
   echo "Example:" 
   echo "\t./plugins/lumen_plugin/deploy.sh --environment=local --install_dependencies=True"
   echo
}
################################################################################
# Deploy Locally                                                               #
################################################################################
Local_Deploy()
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
# Start Webserver and Scheduler                                                #
################################################################################
Start_Airflow()
{
  if [$environment="Ubuntu"]
  then
    x-terminal-emulator --window-with-profile="$(id -u)" --working-directory=$(pwd) -e "echo -e \"\n\n\nStarting webserver...\";. \"bin/activate\"; airflow webserver"
    x-terminal-emulator --window-with-profile="$(id -u)" --working-directory=$(pwd) -e "echo -e \"\n\n\nStarting scheduler...\";. \"bin/activate\"; airflow scheduler"
  else
    osascript -e 'tell app "Terminal"
      do script "echo -e \"\n\n\nStarting webserver...\";. \"bin/activate\"; airflow webserver"
    end tell's
    osascript -e 'tell app "Terminal"
      do script "echo -e \"\n\n\nStarting scheduler...\";. \"bin/activate\"; airflow scheduler"
    end tell'

}
################################################################################
################################################################################
# Main program                                                                 #
################################################################################
################################################################################
################################################################################
# Process the input options. Add options as needed.                            #
################################################################################
# Get the options

while [ $# -gt 0 ]; do
  case "$1" in
    --help)
      Help
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
      Help
      exit 1
  esac
  shift
done

Local_Deploy
Start_Airflow

printf "environment is set to %s\n" "$environment"
printf "install_dependencies is set to %s\n" "$install_dependencies"
printf "operating_system is set to %s\n" "$operating_system"