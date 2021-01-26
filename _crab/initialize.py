import typing

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class VaultClient:
    def __init__(self, vault_name: str):
        self.vault_name = vault_name
        self.credential: typing.Union[DefaultAzureCredential, None] = None
        self.secret_client: typing.Union[SecretClient, None] = None

    @classmethod
    def get_client(cls, vault_name: str) -> 'VaultClient':
        client = cls(vault_name)
        client.login()
        client.init_vault()
        return client

    def login(self):
        self.credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    def init_vault(self):
        vault_url = f'https://{self.vault_name}.vault.azure.net/'
        self.secret_client = SecretClient(vault_url=vault_url, credential=self.credential)
