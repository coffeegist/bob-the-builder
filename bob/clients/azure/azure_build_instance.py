import json

class AzureBuildInstance():
    NAME_KEY = "name"
    QUEUE_TIME_VARIABLES_KEY = "queue_time_variables"
    TAGS_KEY = "tags"


    def __init__(self, name="Default"):
        self._name = name
        self._queue_time_variables = {}
        self._tags = []


    def get_name(self):
        return self._name


    def get_queue_time_variables(self):
        return self._queue_time_variables


    def get_tags(self):
        return self._tags


    def add_queue_time_variable(self, key, value):
        self._queue_time_variables[key] = value


    def add_tag(self, tag):
        self._tags.append(tag)


    def add_tags(self, tag_list):
        self._tags += tag_list


    def to_dict(self):
        dict = {
            AzureBuildInstance.NAME_KEY: self._name,
            AzureBuildInstance.QUEUE_TIME_VARIABLES_KEY: {},
            AzureBuildInstance.TAGS_KEY: self._tags
        }
        for key, value in self._queue_time_variables.items():
            try:
                value = json.loads(value)
            except ValueError:
                pass
            dict[AzureBuildInstance.QUEUE_TIME_VARIABLES_KEY][key] = value
        return dict


    @staticmethod
    def from_dict(dict):
        build_instance = AzureBuildInstance(dict[AzureBuildInstance.NAME_KEY])
        build_instance.add_tags(dict[AzureBuildInstance.TAGS_KEY])
        for key, value in dict[AzureBuildInstance.QUEUE_TIME_VARIABLES_KEY].items():
            try:
                if (not isinstance(value, str)):
                    value = json.dumps(value)
            except ValueError:
                pass
            build_instance.add_queue_time_variable(key, value)
        return build_instance
