# Python script to update API versions in Azure Resource Manager templates
"""
Copyright (c) 2016, Guy Bowerman
Description: Graphical dashboard to show and set Azure VM Scale Set properties
License: MIT (see LICENSE.txt file for details)
"""
import json
import sys
import os.path
from collections import OrderedDict

# update this list to current versions before running the script
computeApiVersion = '2016-03-30'
networkApiVersion = '2016-03-30'
storageApiVersion = '2015-06-15'
insightsApiVersion = '2015-04-01'

overprovisionValue = 'true' # set VMSS overprovision value, default is true

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

# loop through resources setting current API versions
for resource in templateData['resources']:
    if resource['type'].startswith('Microsoft.Compute'):
        containsComputeResource = True
        resource['apiVersion'] = "[variables('computeApiVersion')]"
        if resource['type'] == 'Microsoft.Compute/virtualMachineScaleSets':
            resource['properties']['overprovision'] = 'true'

    elif resource['type'].startswith('Microsoft.Network'):
        containsNetworkResource = True
        resource['apiVersion'] = "[variables('networkApiVersion')]"

    elif resource['type'].startswith('Microsoft.Storage'):
        containsStorageResource = True
        resource['apiVersion'] = "[variables('storageApiVersion')]"

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

