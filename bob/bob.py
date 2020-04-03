import argparse

from menu import Menu
from clients.client_factory import ClientFactory


def get_client(client_name, config_file):
    return ClientFactory.get_client(client_name, config_file)


def configure_cmd(args):
    blueprints = []

    while True:
        blueprints.extend(args._client.create_blueprints())
        args._client.save_blueprints(blueprints, args.filename)
        if not Menu.yes_or_no("\nAdd another job?"):
            break


def run_cmd(args):
    blueprints = args._client.load_blueprints(args.filename)

    for blueprint in blueprints:
        args._client.execute_blueprint(blueprint, args.output_directory)


def main():
    parser = argparse.ArgumentParser(description='Bob the Builder')
    parser.add_argument('-c', '--config', metavar='FILE',
        required=False, default='bob-config.json', help='Bob config file location')

    subparsers = parser.add_subparsers()

    # "configure"
    configure_parser = subparsers.add_parser('configure', help="Generate a blueprint for future jobs")
    configure_parser.set_defaults(dispatch=configure_cmd)
    configure_parser.add_argument('-f', '--filename', metavar='FILE',
        required=True, help='File to write blueprint to')

    # "run"
    run_parser = subparsers.add_parser('run', help="Queue a pre-generated blueprint")
    run_parser.set_defaults(dispatch=run_cmd)
    run_parser.add_argument('-f', '--filename', metavar='FILE',
        required=True, help='File to read blueprint from')
    run_parser.add_argument('-o', '--output-directory', metavar='DIR',
        required=False, default='.', help='Directory to output artifacts to')

    args = parser.parse_args()
    args._client = get_client('Azure', args.config)

    if 'dispatch' in args:
        cmd = args.dispatch
        del args.dispatch
        cmd(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
