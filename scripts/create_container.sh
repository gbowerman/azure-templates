#!/bin/bash
# script to create a storage account with SAS URI
SANAME=$1
RGNAME=$2
LOCATION=$3
CONTAINERNAME=$4

SASSTART=`date +%Y-%m-%d`'T00:00:00Z'
EXPIRY=`date -d "+30 days" +%Y-%m-%d`'T00:00:00Z'
SASNAME=$CONTAINERNAME'sas'

# create the resource group (keeps going if already exists)
az group create --name $RGNAME --location $LOCATION

# Create a storage account (keeps going if already exists)
az storage account create --name $SANAME --resource-group $RGNAME

# Get a storage account key:
KEY=`az storage account keys list -g $RGNAME -n $SANAME | jq .[0].value`

# Create a container using the key:
az storage container create -n $CONTAINERNAME --account-name $SANAME --account-key $KEY

# Create a SAS token on the container and get the key
SASKEY=`az storage blob generate-sas --account-name $SANAME --account-key $KEY --container-name $CONTAINERNAME \
    --permissions w --start $SASSTART --expiry $EXPIRY --name $SASNAME`

# remove quotes
SASKEY=${SASKEY:1:-1}

# return the SAS URI
echo 'https://'$SANAME'.blob.core.windows.net/'$CONTAINERNAME'?'$SASKEY

