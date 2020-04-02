import json
import pprint

class AzureBlueprint():
    TYPE_KEY = "__type__"
    PROJECT_KEY = "project"
    DEFINITION_KEY = "definition"
    SOURCE_BRANCH_KEY = "source_branch"

    def __init__(self, project=None, definition=None):
        self._type = 'NONE'
        self._project = project
        self._definition = definition
        self._source_branch = 'master'

    def get_actions(self):
        return self._actions


    def set_actions(self, actions):
        self._actions = actions


    def get_project(self):
        return self._project


    def set_project(self, project):
        self._project = project


    def get_definition(self):
        return self._definition


    def set_definition(self, definition):
        self._definition = definition


    def get_source_branch(self):
        return self._source_branch


    def set_source_branch(self, branch):
        self._source_branch = branch


    def save_to_file(self, filename):
        file_data = self.to_dict()
        with open(filename, 'w') as config_fp:
            json.dump(file_data, config_fp, sort_keys=True, indent=4)


    def to_dict(self):
        dict = {
            AzureBlueprint.TYPE_KEY: type(self).__name__,
            AzureBlueprint.PROJECT_KEY: self._project,
            AzureBlueprint.DEFINITION_KEY: self._definition,
            AzureBlueprint.SOURCE_BRANCH_KEY: self._source_branch
        }

        return dict


    def populate_from_dict(self, config):
        if AzureBlueprint.PROJECT_KEY in config.keys():
            self._project = config[AzureBlueprint.PROJECT_KEY]
        if AzureBlueprint.DEFINITION_KEY in config.keys():
            self._definition = config[AzureBlueprint.DEFINITION_KEY]
        if AzureBlueprint.SOURCE_BRANCH_KEY in config.keys():
            self._source_branch = config[AzureBlueprint.SOURCE_BRANCH_KEY]


    @staticmethod
    def save_blueprints_to_file(blueprints, filename):
        file_data = []
        for blueprint in blueprints:
            file_data.append(blueprint.to_dict())

        with open(filename, 'w') as config_fp:
            json.dump(file_data, config_fp, sort_keys=True, indent=4)


    @staticmethod
    def load_from_file(filename):
        data = None
        blueprints = []
        blueprint_type_map = {}

        for blueprint_type in AzureBlueprint.__subclasses__():
            blueprint_type_map[blueprint_type.__name__] = blueprint_type

        with open(filename) as data_fp:
            data = json.load(data_fp)

        if type(data) != list:
            data = [data]

        for config in data:
            if AzureBlueprint.TYPE_KEY in config.keys():
                blueprint_type = config[AzureBlueprint.TYPE_KEY]
                if blueprint_type in blueprint_type_map.keys():
                    blueprint = blueprint_type_map[blueprint_type]()
                    blueprint.populate_from_dict(config)
                    blueprints.append(blueprint)
                else:
                    print("Unknown blueprint type: {}".format(blueprint_type))

        return blueprints
