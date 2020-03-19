from config import Config
from clients.azure.azure_client import AzureClient

class ClientFactory():
    _client_map = {
        'Azure': AzureClient
    }

    def get_client_list():
        return list(ClientFactory._client_map.keys())

    def get_client(client_name, config_file):
        client_type = ClientFactory._client_map[client_name]
        return client_type(ClientFactory._get_config(config_file))

    def _get_config(config_file):
        return Config(config_file)
