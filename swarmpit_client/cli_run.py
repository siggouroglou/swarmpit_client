import configparser
import click

from swarmpit_client.operations import SwarmpitOperation


@click.command()
@click.option("-c", "--config", help="Set your config file")
def cli_run(config):
    if not config:
        print("ERROR: You must specify a configuration file, using the argument '-c' or '--config'.")
        exit(10)

    # Get the config ini file
    parser = configparser.ConfigParser()
    parser.read(config)

    # Initialize an operation
    operation = parser.get("operation", "name")
    swarmpit_op = SwarmpitOperation(parser.get("swarmpit", "url"), parser.get("swarmpit", "auth"))

    # Run the requested operation
    if operation == "update_service_version":
        data = {
            "repository": {
                "name": parser.get("operation", "service_repo_name"),
                "tag": parser.get("operation", "service_repo_tag")
            }
        }
        swarmpit_op.update_service_version(parser.get("operation", "service_name"), data)
    elif operation == "redeploy_service":
        swarmpit_op.redeploy_service(
            parser.get("operation", "service_name"),
            parser.get("operation", "service_repo_tag")
        )
    else:
        print("ERROR: Not valid operation")
        exit(11)
