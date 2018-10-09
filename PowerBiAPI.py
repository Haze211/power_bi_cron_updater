
# coding: utf-8

# In[3]:


import adal
from pypowerbi.dataset import Column, Table, Dataset
from pypowerbi.client import PowerBIClient
import requests
from power_bi_updater_config import client_id, username, password

authority_url = 'https://login.windows.net/common'
resource_url = 'https://analysis.windows.net/powerbi/api'
api_url = 'https://api.powerbi.com'

context = adal.AuthenticationContext(authority=authority_url,
                                     validate_authority=True,
                                     api_version=None)


# In[5]:


token = context.acquire_token_with_username_password(resource=resource_url,
                                                     client_id=client_id,
                                                     username=username,
                                                     password=password)


# In[6]:


client = PowerBIClient(api_url, token)
print("Client Initialized")


# In[7]:


def refresh_dataset(client_obj, dataset_id, notify_option=None, group_id=None):
        """
        Refreshes a single dataset
        :param dataset_id: The id of the dataset to refresh
        :param notify_option: The optional notify_option to add in the request body
        :param group_id: The optional id of the group
        """
        
        client = client_obj
        datasets_snippet = 'datasets'
        refreshes_snippet = 'refreshes'
        
        base_url = f'{client.api_url}/{client.api_version_snippet}/{client.api_myorg_snippet}'
        
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{groups_snippet}/{group_id}/'
        
        
        
        # form the url
        url = f'{base_url}{groups_part}/{datasets_snippet}/{dataset_id}/{refreshes_snippet}'

        # form the headers
        headers = client.auth_header

        if notify_option is not None:
            json_dict = {
                'notifyOption': notify_option
            }
        else:
            json_dict = None

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 202:
            raise HTTPError(response, f'Refresh dataset request returned http error: {response.status_code}')


# In[8]:


refresh_dataset(client, "7f212b59-bccf-4f44-bf3b-318701abac50")
print("Report Updated")

