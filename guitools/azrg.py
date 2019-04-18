'''azrg - GUI tool to manage Azure resource groups'''
import os
from tkinter import *
import tkinter

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv

# load Azure environment and start a client connection
load_dotenv()
subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
)
client = ResourceManagementClient(credentials, subscription_id)

# declare TK resources
window = Tk()
rglistbox = Listbox(window)
statuslbl = Label(window, text="Select a resource group")

def deleterg():
    '''Delete the selected resource groups'''
    selected = rglistbox.curselection()
    if selected:
        for index in selected:
            rgname = rglistbox.get(index)
            print(f'About to delete: {rgname}')
            delete_op = client.resource_groups.delete(rgname)
            status = f'{rgname} delete returned {delete_op.response}'
            statuslbl.configure(text=status)

deletebtn = Button(window, text="Delete", command=deleterg, bg='#F8F8FF')


def load_resource_groups(client, listbox):
    '''List Azure resource groups and load them into a TK listbox'''
    # list resource groups
    idx = 1
    for item in client.resource_groups.list():
        #print(f'{item.name} - {item.location}')
        listbox.insert(idx, item.name)
        idx += 1


def main():
    '''main routine - start by customizing GUI'''
    window.title('Azure resource group tool')
    window.geometry('350x200')
    window.configure(background='#B0E0E6')
    rglistbox.grid(column=0, row=0)
    load_resource_groups(client, rglistbox) 
    deletebtn.grid(column=1, row=0)
    statuslbl.grid(column=0, row=1)
    
    window.mainloop()


if __name__ == "__main__":
    main()
