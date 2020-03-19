import argparse

from menu import Menu
from bob_build import BobBuild
from clients.client_factory import ClientFactory


def get_client(client_name, config_file):
    return ClientFactory.get_client(client_name, config_file)


def configure_cmd(args):
    blueprints = []

    while True:
        blueprints.append(args._client.create_blueprint())
        args._client.save_blueprints(blueprints, args.filename)
        if not Menu.yes_or_no("Add another job?"):
            break


def run_cmd(args):
    blueprints = args._client.load_blueprints(args.filename)

    for blueprint in blueprints:
        bob_builds = args._client.build_blueprint(blueprint)
        for build in bob_builds:
            if build.is_build_successful():
                args._client.download_build_artifacts(build.original_build, args.output_directory, build.name)


def main():
    parser = argparse.ArgumentParser(description='Bob the Azure Builder')
    parser.add_argument('-c', '--config', metavar='FILE',
        required=False, default='bob-config.json', help='Bob config file location')

    # service selection
    service = parser.add_mutually_exclusive_group(required=True)
    service.add_argument("--azure", action='store_true', help="Use Azure for your builds.")

    subparsers = parser.add_subparsers()

    # "configure"
    configure_parser = subparsers.add_parser('configure', help="Generate a BlueprintProducer configuration file for future builds")
    configure_parser.set_defaults(dispatch=configure_cmd)
    configure_parser.add_argument('-f', '--filename', metavar='FILE',
        required=True, help='File to write build configuration to')

    # "run"
    run_parser = subparsers.add_parser('run', help="Queue a build for a pre-generated BlueprintProducer configuration")
    run_parser.set_defaults(dispatch=run_cmd)
    run_parser.add_argument('-f', '--filename', metavar='FILE',
        required=True, help='File to read build configuration from')
    run_parser.add_argument('-o', '--output-directory', metavar='DIR',
        required=False, default='.', help='Directory to output build artifacts to')

    args = parser.parse_args()

    if args.azure:
        args._client = get_client('Azure', args.config)
        del args.azure

    if 'dispatch' in args:
        cmd = args.dispatch
        del args.dispatch
        cmd(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
