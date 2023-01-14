from swarmpit_client.api_client import SwarmpitAPIClient


class SwarmpitOperation:

    def __init__(self, base_url: str, authorization: str):
        self.swarmpit_client = SwarmpitAPIClient(base_url, authorization)

    def update_service_version(self, service_name: str, service_data: dict):
        service = self.swarmpit_client.service_get_by_name(service_name)

        # If service not exists, create it
        if not service:
            service = self.swarmpit_client.service_create(service_data)
            if service is None:
                exit(20)

        service = self.swarmpit_client.service_update(service_name, service_data)
        if service is None:
            exit(21)

    def redeploy_service(self, service_name: str, service_tag: str):
        service = self.swarmpit_client.service_redeploy(service_name, service_tag)
        if service is None:
            exit(21)
