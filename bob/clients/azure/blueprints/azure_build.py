import json
import pprint

from .azure_blueprint import AzureBlueprint
from .build_instance import AzureBuildInstance

class AzureBuild(AzureBlueprint):
    RESULT_SUCCESS = "succeeded"

    BUILD_INSTANCES_KEY = "build_instances"
    AGENT_QUEUE_KEY = "agent_queue"
    AGENT_SPECIFICATION_KEY = "agent_specification"
    DOWNLOAD_ARTIFACTS_KEY = "download_artifacts"


    def __init__(self):
        super().__init__()
        self._build_instances = []
        self._agent_queue = None
        self._agent_specification = None
        self._download_artifacts = True


    def get_agent_queue(self):
        return self._agent_queue


    def set_agent_queue(self, agent_queue):
        self._agent_queue = agent_queue


    def get_agent_specification(self):
        return self._agent_specification


    def set_agent_specification(self, agent_specification):
        self._agent_specification = agent_specification


    def get_build_instances(self):
        return self._build_instances


    def get_download_artifacts(self):
        return self._download_artifacts


    def set_download_artifacts(self, download_artifacts):
        self._download_artifacts = download_artifacts


    def add_build_instance(self, build_instance):
        self._build_instances.append(build_instance)


    def to_dict(self):
        dict = super().to_dict()

        updates = {
            AzureBuild.AGENT_QUEUE_KEY: self._agent_queue,
            AzureBuild.AGENT_SPECIFICATION_KEY: self._agent_specification,
            AzureBuild.DOWNLOAD_ARTIFACTS_KEY: self._download_artifacts,
            AzureBuild.BUILD_INSTANCES_KEY: []
        }

        for build_instance in self._build_instances:
            updates[AzureBuild.BUILD_INSTANCES_KEY].append(build_instance.to_dict())

        dict.update(updates)

        return dict


    def populate_from_dict(self, config):
        super().populate_from_dict(config)

        if AzureBuild.AGENT_QUEUE_KEY in config.keys():
            self._agent_queue = config[AzureBuild.AGENT_QUEUE_KEY]
        if AzureBuild.AGENT_SPECIFICATION_KEY in config.keys():
            self._agent_specification = config[AzureBuild.AGENT_SPECIFICATION_KEY]
        if AzureBuild.DOWNLOAD_ARTIFACTS_KEY in config.keys():
            self._download_artifacts = config[AzureBuild.DOWNLOAD_ARTIFACTS_KEY]

        if AzureBuild.BUILD_INSTANCES_KEY in config.keys():
            for instance in config[AzureBuild.BUILD_INSTANCES_KEY]:
                build_instance = AzureBuildInstance.from_dict(instance)
                self.add_build_instance(build_instance)
                build_instance = None
