from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from crab.common import activate_azure_env, list_azure_env, destroy_azure_env


class BaseClient:
    def __init__(self):
        self.credential = None
        self.secret_client = None

    def login(self):
        self.credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    def init_vault(self, vault_name: str):
        vault_url = f'https://{vault_name}.vault.azure.net/'
        self.secret_client = SecretClient(vault_url=vault_url, credential=self.credential)


if __name__ == '__main__':
    # activate_azure_env('test')
    print(list_azure_env())
    destroy_azure_env('test')
    # client = BaseClient()
    # name = input('Vault name: ')
    # client.login()
    # client.init_vault(name)
    # print(client.credential)
    # secret_properties = client.secret_client.list_properties_of_secrets()
    #
    # for secret_property in secret_properties:
    #     # the list doesn't include values or versions of the secrets
    #     print(secret_property.name)