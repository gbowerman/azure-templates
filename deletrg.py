'''delete_rg.py - example script to delete an Azure Resource Group'''
import json
import os
import sys

import azurerm    


def main():
    '''Main routine.'''
    # check for single command argument
    if len(sys.argv) != 2:
        sys.exit('Usage: python ' + sys.argv[0] + ' rg_name')

    rgname = sys.argv[1]

    # if in Azure cloud shell, authenticate using the MSI endpoint
    if 'ACC_CLOUD' in os.environ and 'MSI_ENDPOINT' in os.environ:
        access_token = azurerm.get_access_token_from_cli()
        subscription_id = azurerm.get_subscription_from_cli()
    else: # load service principal details from a config file        
        try:
            with open('azurermconfig.json') as configfile:
                configdata = json.load(configfile)
        except FileNotFoundError:
            sys.exit('Error: Expecting azurermconfig.json in current folder')

        tenant_id = configdata['tenantId']
        app_id = configdata['appId']
        app_secret = configdata['appSecret']
        if subscription_id is None:
            subscription_id = configdata['subscriptionId']

        # authenticate
        access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

    # delete a resource group
    rgreturn = azurerm.delete_resource_group(access_token, subscription_id, rgname)
    print(rgreturn)


if __name__ == "__main__":
    main()