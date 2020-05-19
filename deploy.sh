#!/bin/sh
################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "This script will deploy the lumen plugin to an environment, using the instructions listed in the README.md file."
   echo
   echo "Example: .plugins/lumen_plugin/deploy.sh --environment=local --install_dependencies=True"
   echo
   echo "Required parameters:"
   echo "environment               The environment you'd like to deploy to. (local, astronomer, google_cloud_composer)"
   echo "install_dependencies      Whether you want a fresh install of Lumen plugin. This will import all necessary depencies for the environment chosen (True, False)"
   echo
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
    *)
      printf "***************************\n"
      printf "Error: Invalid argument.\n\""
      printf $1
      printf "\" is not defined.\n"
      printf "***************************\n"
      Help
      exit 1
  esac
  shift
done

printf "Argument environment is %s\n" "$environment"
printf "Argument install_dependencies is %s\n" "$install_dependencies"