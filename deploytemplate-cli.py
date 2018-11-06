''' deploytemplate.py - simple commandline deployment of a github template'''
# Takes a deployment template URI and a local parameters file and deploys it
# to do:
# - checkin to a github repo
import argparse
import azurerm
from haikunator import Haikunator
import json
import sys


def main():
    '''Main routine.'''

    # validate command line arguments
    argParser = argparse.ArgumentParser()

    argParser.add_argument('--uri', '-u', required=True,
                           action='store', help='Template URI')
    argParser.add_argument('--params', '-p', required=True,
                           action='store', help='Parameters json file')
    argParser.add_argument('--location', '-l', required=True,
                           action='store', help='Location, e.g. eastus')
    argParser.add_argument('--rg', '-g', required=False,
                           action='store', help='Resource Group name')
    argParser.add_argument('--sub', '-s', required=False,
                           action='store', help='Subscription ID')

    args = argParser.parse_args()

    template_uri = args.uri
    params = args.params
    rgname = args.rg
    location = args.location
    subscription_id = args.sub

    # load parameters file
    try:
        with open(params) as params_file:
            param_data = json.load(params_file)
    except FileNotFoundError:
        sys.exit('Error: Expecting ' + params + ' in current folder')

    # prep Haikunator
    haikunator = Haikunator()

    # get a current access token from your local Azure CLI environment
    access_token = azurerm.get_access_token_from_cli()
    if subscription_id is None:
        subscription_id = azurerm.get_subscription_from_cli()

    # create resource group if not specified
    if rgname is None:
        rgname = haikunator.haikunate()
        ret = azurerm.create_resource_group(access_token, subscription_id, rgname, location)
        print(ret)
    print('Resource group:' + rgname)

    deployment_name = haikunator.haikunate() 
    print('Deployment name:' + deployment_name)

    # deploy template and print response
    deploy_return = azurerm.deploy_template_uri(
        access_token, subscription_id, rgname, deployment_name, template_uri, param_data)

    print(json.dumps(deploy_return.json(), sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    main()
