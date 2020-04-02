from azure.devops.credentials import BasicAuthentication
from azure.devops.connection import Connection

from menu import Menu
from .blueprints import *

class AzureBlueprintFactory():


    def __init__(self, connection):
        self._connection = connection
        self._BLUEPRINT_ACTION_MAP = {
            'Build' : self.create_build_blueprints,
            'Download' : self.create_download_blueprints
        }


    def create_blueprints(self):
        project = self._select_project()
        action = self._select_action()

        return self._BLUEPRINT_ACTION_MAP[action](project)


    def create_build_blueprints(self, project):
        blueprints = []
        definitions = self._select_definition(project, multiple=True)
        for definition in definitions:
            print("\n--- Configuring {} ---".format(definition.name))
            azure_blueprint = AzureBuild()
            azure_blueprint.set_project(project.name)
            azure_blueprint.set_definition(definition.name)
            azure_blueprint.add_build_instance(
                self._select_definition_queue_time_variables(definition))

            if Menu.yes_or_no('Use default agent queue?'):
                agent_queue = definition.queue
            else:
                agent_queue = self._select_agent_queue(project)

            azure_blueprint.set_agent_queue(agent_queue.name)

            if Menu.yes_or_no('Use default agent specification?'):
                try:
                    agent_specification = (definition.additional_properties
                        ['process']['target']['agentSpecification']['identifier'])
                except:
                    agent_specification = None
            else:
                agent_specification = self._select_agent_specification(agent_queue)

            azure_blueprint.set_agent_specification(agent_specification)

            if Menu.yes_or_no('Download build artifacts?'):
                azure_blueprint.set_download_artifacts(True)
            else:
                azure_blueprint.set_download_artifacts(False)

            blueprints.append(azure_blueprint)

        return blueprints


    def create_download_blueprints(self, project):
        blueprints = []
        definitions = self._select_definition(project, multiple=True)
        for definition in definitions:
            azure_blueprint = AzureDownload()
            azure_blueprint.set_project(project.name)
            azure_blueprint.set_definition(definition.name)
            blueprints.append(azure_blueprint)

        return blueprints


    def load_blueprints(self, filename):
        return AzureBlueprint.load_from_file(filename)


    def _select_project(self):
        core_client = self._connection.clients.get_core_client()
        projects = core_client.get_projects()
        print("\n-- Projects --")
        return Menu.choose_from_list(projects, "project")


    def _select_definition(self, project, multiple=False):
        build_client = self._connection.clients_v5_1.get_build_client()
        definitions = build_client.get_definitions(project.name, include_all_properties=True)
        print("\n-- Definitions --")
        if multiple:
            return Menu.choose_multiple_from_list(definitions, "definition")
        else:
            return Menu.choose_from_list(definitions, "definition")


    def _select_agent_pool(self, project):
        task_agent_client = self._connection.clients.get_task_agent_client()
        agent_pools = task_agent_client.get_agent_pools()
        print("\n-- Agent Pools --")
        return Menu.choose_from_list(agent_pools, "Agent Pool")


    def _select_action(self):
        print("\n-- Actions --")
        return Menu.choose_from_list(
            list(self._BLUEPRINT_ACTION_MAP.keys()), "action", None
        )


    def _select_agent_queue(self, project):
        task_agent_client = self._connection.clients_v5_1.get_task_agent_client()
        agent_queues = task_agent_client.get_agent_queues(project.id)
        print("\n-- Agent Queues --")
        return Menu.choose_from_list(agent_queues, "Agent Queue")


    def _select_agent_specification(self, queue):
        # Agent strings should not change according to guy @ microsoft
        # https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops

        agent_specification = Menu.choose_from_list([
            "windows-latest",
            "windows-2019",
            "vs2017-win2016",
            "vs2015-win2012r2",
            "win1803",
            "ubuntu-latest",
            "ubuntu-16.04",
            "macOS-latest",
            "macOS-10.14",
            "macOS-10.13"
        ], "Agent Specifications", field=None)

        return agent_specification


    def _select_definition_queue_time_variables(self, definition):
        azure_build_instance = AzureBuildInstance(name="Default")

        if "variables" in definition.additional_properties:
            for key, value in definition.additional_properties["variables"].items():
                if "allowOverride" in value:
                    if value["allowOverride"]:
                        azure_build_instance.add_queue_time_variable(key, value["value"])

        return azure_build_instance
