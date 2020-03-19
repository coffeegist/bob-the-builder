import json
import pprint

from .azure_build_instance import AzureBuildInstance

class AzureBlueprint():
    PROJECT_KEY = "project"
    DEFINITION_KEY = "definition"
    BUILD_INSTANCES_KEY = "build_instances"
    AGENT_QUEUE_KEY = "agent_queue"
    AGENT_SPECIFICATION_KEY = "agent_specification"
    SOURCE_BRANCH_KEY = "source_branch"


    def __init__(self, project=None, definition=None, build_instances=None,
                    agent_queue=None, agent_specification=None, source_branch='master'):
        self._project = project
        self._definition = definition
        if build_instances == None:
            self._build_instances = []
        else:
            self._build_instances = build_instances
        self._agent_queue = agent_queue
        self._agent_specification = agent_specification
        self._source_branch = source_branch


    def get_project(self):
        return self._project


    def set_project(self, project):
        self._project = project


    def get_definition(self):
        return self._definition


    def set_definition(self, definition):
        self._definition = definition


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


    def get_source_branch(self):
        return self._source_branch


    def set_source_branch(self, branch):
        self._source_branch = branch


    def add_build_instance(self, build_instance):
        self._build_instances.append(build_instance)


    def save_to_file(self, filename):
        file_data = self.to_dict()
        with open(filename, 'w') as config_fp:
            json.dump(file_data, config_fp, sort_keys=True, indent=4)


    def to_dict(self):
        dict = {
            AzureBlueprint.PROJECT_KEY: self._project,
            AzureBlueprint.DEFINITION_KEY: self._definition,
            AzureBlueprint.AGENT_QUEUE_KEY: self._agent_queue,
            AzureBlueprint.AGENT_SPECIFICATION_KEY: self._agent_specification,
            AzureBlueprint.SOURCE_BRANCH_KEY: self._source_branch,
            AzureBlueprint.BUILD_INSTANCES_KEY: []
        }

        for build_instance in self._build_instances:
            dict[AzureBlueprint.BUILD_INSTANCES_KEY].append(build_instance.to_dict())

        return dict


    @staticmethod
    def save_blueprints_to_file(blueprints, filename):
        file_data = []
        for blueprint in blueprints:
            file_data.append(blueprint.to_dict())

        with open(filename, 'w') as config_fp:
            json.dump(file_data, config_fp, sort_keys=True, indent=4)


    @staticmethod
    def load_from_file(filename):
        blueprints = []
        data = None
        with open(filename) as data_fp:
            data = json.load(data_fp)

        if type(data) != list:
            data = [data]

        for config in data:
            blueprint = AzureBlueprint()

            if AzureBlueprint.PROJECT_KEY in config.keys():
                blueprint._project = config[AzureBlueprint.PROJECT_KEY]
            if AzureBlueprint.DEFINITION_KEY in config.keys():
                blueprint._definition = config[AzureBlueprint.DEFINITION_KEY]
            if AzureBlueprint.AGENT_QUEUE_KEY in config.keys():
                blueprint._agent_queue = config[AzureBlueprint.AGENT_QUEUE_KEY]
            if AzureBlueprint.AGENT_SPECIFICATION_KEY in config.keys():
                blueprint._agent_specification = config[AzureBlueprint.AGENT_SPECIFICATION_KEY]
            if AzureBlueprint.SOURCE_BRANCH_KEY in config.keys():
                blueprint._source_branch = config[AzureBlueprint.SOURCE_BRANCH_KEY]

            if AzureBlueprint.BUILD_INSTANCES_KEY in config.keys():
                for instance in config[AzureBlueprint.BUILD_INSTANCES_KEY]:
                    build_instance = AzureBuildInstance.from_dict(instance)
                    blueprint.add_build_instance(build_instance)
                    build_instance = None

            blueprints.append(blueprint)

        return blueprints
