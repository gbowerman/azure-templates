# deploytemplate.py
Python program to deploy an Azure template from a github repo, with a local parameters.json file

If running in an Azure cloud shell the program will authenticate to Azure using an MSI endpoint.

If running in other environemnts create an azurermtemplate.json to authenticate.

To call this program, see the example shell scripts: runit.sh, runwait.sh (waits for deployment to complete), debugrun.sh.

# Tools to cleanup resources
listrg.py - list Azure resource groups

deleterg.py - delete the specified Azure resource group

# apiupgradeer.py - Template API updater
Python script to update API versions in Azure Resource Manager templates

This script will create API version variables for Compute, Network, Storage, Insights resources, and set each resource type to the appropriate API version. Use it when you need to upgrade an Azure Resource Manager template to a new API version for one or more resources.

The script also adds an "overprovision" property to any Microsoft.Compute/virtualMachineScaleSets resources if not present. This property is set to true.


## Installation and Usage
  1. Install Python 3.x.
  2. Clone this repo locally or just copy apiUpgrader.py and run it locally
  3. Make sure the apiUpgrader file has current API versions set for Azure resources like Compute, Storage, Network, Insights. Edit the file as needed.
  4. Usage: python apiUpgrader.py inputfile.json > outputfile.json
  5. Inspect the output file. If the original version had a variable defined like "apiVersion" it may no longer be needed. Check the variables section of the template for any variables which are no longer referenced.
  6. If your template has VM Scale Set resources and you don't want the default overprovision behavior, set the overprovision property to "false".
  7. Do a successful test deployment of the template before declaring it upgraded.


