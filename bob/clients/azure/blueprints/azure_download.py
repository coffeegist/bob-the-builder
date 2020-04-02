import json
import pprint

from .azure_blueprint import AzureBlueprint

class AzureDownload(AzureBlueprint):
    TAGS_KEY = "tags"

    def __init__(self):
        super().__init__()
        self._tags = []


    def get_tags(self):
        return self._tags


    def set_tags(self, tags):
        self._tags = tags


    def add_tag(self, tag):
        self._tags.append(tag)


    def to_dict(self):
        dict = super().to_dict()

        updates = {
            AzureDownload.TAGS_KEY: self._tags
        }

        dict.update(updates)

        return dict


    def populate_from_dict(self, config):
        super().populate_from_dict(config)

        if AzureDownload.TAGS_KEY in config.keys():
            self._tags = config[AzureDownload.TAGS_KEY]
