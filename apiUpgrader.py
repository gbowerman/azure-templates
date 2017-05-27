# Python script to update API versions in Azure Resource Manager templates and make simple compatibility updates
#
# Usage: python apiUpgrader.py source_template.json > output_template.json
#
# Note: The script won't catch everything, for example extensions which make references based on earlier APIs.
# The script will also make mistakes if your source template sets advanced properties that the script didn't check for.
# Thereforee check the output manually and test before relying on the output scripts.
#
# Author: guybo@outlook.com
#
# Last update 5/27/2017

from collections import OrderedDict
import json
import sys
import os.path

# update this list to current versions before running the script
computeApiVersion = '2017-03-30'
networkApiVersion = '2017-04-01'
storageApiVersion = '2016-01-01'
insightsApiVersion = '2015-04-01'

overprovision_value = 'true'  # default overprovision value for VMSS

# booleans which get switched on when a resource is discovered
containsComputeResource = False
containsNetworkResource = False
containsStorageResource = False
containsInsightsResource = False


def usage():
    sys.exit('Usage: python ' + sys.argv[0] + ' filename')


# check for single command argument representing template filename
if len(sys.argv) != 2:
    usage()

templateFileStr = sys.argv[1]

# check file exists
if os.path.isfile(templateFileStr) is False:
    print('File not found: ' + templateFileStr)
    usage()

# Load JSON template file
try:
    with open(templateFileStr) as templateFile:
        templateData = json.load(templateFile, object_pairs_hook=OrderedDict)
except FileNotFoundError:
    print("Error: " + templateFile + " file not found.")
    sys.exit()

# templateData is now loaded with the ARM template, with order preserved

# loop through resources setting current API versions and making any
# compatibility upgrades
for resource in templateData['resources']:
    if resource['type'].startswith('Microsoft.Compute'):
        containsComputeResource = True
        resource['apiVersion'] = "[variables('computeApiVersion')]"
        if resource['type'] == 'Microsoft.Compute/virtualMachineScaleSets':
            if 'overprovision' not in resource['properties']:
                resource['properties']['overprovision'] = overprovision_value

    elif resource['type'].startswith('Microsoft.Network'):
        containsNetworkResource = True
        resource['apiVersion'] = "[variables('networkApiVersion')]"

    elif resource['type'].startswith('Microsoft.Storage'):
        containsStorageResource = True
        resource['apiVersion'] = "[variables('storageApiVersion')]"
        resource['kind'] = "Storage"
        resource['properties'] = {}
        resource['sku'] = {"name": "[variables('storageAccountType')]"}

    elif resource['type'].startswith('Microsoft.Insights'):
        containsInsightsResource = True
        resource['apiVersion'] = "[variables('insightsApiVersion')]"

# create or overwrite variables for the resource API versions if they exist
if containsComputeResource == True:
    templateData['variables']['computeApiVersion'] = computeApiVersion
if containsNetworkResource == True:
    templateData['variables']['networkApiVersion'] = networkApiVersion
if containsStorageResource == True:
    templateData['variables']['storageApiVersion'] = storageApiVersion
if containsInsightsResource == True:
    templateData['variables']['insightsApiVersion'] = insightsApiVersion

# print the upgraded JSON template to standard out
print(json.dumps(templateData, sort_keys=False, indent=2, separators=(',', ': ')))
