import json
from typing import Optional

import requests as requests


class SwarmpitAPIClient:

    def __init__(self, base_url: str, authorization: str):
        self.url = f"{base_url}/api"
        self.authorization = authorization

    def service_create(self, service_data: dict) -> Optional[dict]:
        headers = {
            "authorization": self.authorization,
            "Content-Type": "application/json; charset=utf-8;"
        }
        r = requests.post(f"{self.url}/services", data=json.dumps(service_data), headers=headers)
        r_data = r.json()

        # Success
        if r.status_code == 201:
            service = service_data
            service["id"] = r_data["id"]
            return service

        # Not success
        print(f"ERROR - service_update - Status: {r.status_code}, Body: {json.dumps(r_data, indent=4)}")
        return None

    def service_update(self, service_name: str, data_to_update: dict) -> Optional[dict]:
        # Get the service from swarmpit
        service_received = self.service_get_by_name(service_name)
        if service_received is None:
            return None

        # Clear its values
        service = {}
        update_required_keys = ("serviceName", "mode", "replicas", "repository", "ports", "resources", "logdriver",
                                "variables", "networks", "labels", "mounts", "hosts", "secrets", "configs",
                                "deployment", "version")
        # "stack", "replicas", "links", "dir", "tty", "containerLabels", "user", "immutable",
        # "command", "agent", "healthcheck")
        for key, value in service_received.items():
            if key in update_required_keys:
                service[key] = value

        # Update the values in service
        for key, value in data_to_update.items():
            service[key] = value
        del service["deployment"]["forceUpdate"]
        del service["deployment"]["rollbackAllowed"]
        mounts = []
        for m in service["mounts"]:
            del m["id"]
            del m["volumeOptions"]
            del m["stack"]
        if service["networks"][0]["serviceAliases"] is None:
            del service["networks"][0]["serviceAliases"]
        service["mounts"] = mounts

        # Update the service in swarmpit
        headers = {
            "authorization": self.authorization,
            "Content-Type": "application/json; charset=utf-8;"
        }
        r = requests.post(f"{self.url}/services/{service_received['id']}", data=json.dumps(service), headers=headers)

        # Success
        if r.status_code == 200:
            return service

        # Not success
        print(f"ERROR - service_update - Status: {r.status_code}, Body: {r.text}")
        return None

    def service_list(self) -> dict:
        headers = {
            "authorization": self.authorization,
            "Content-Type": "application/json; charset=utf-8;"
        }
        r = requests.get(f"{self.url}/services", headers=headers)
        return r.json()

    def service_get_by_name(self, service_name) -> Optional[dict]:
        for d in self.service_list():
            if d["serviceName"] == service_name:
                return d
        return None

    def service_redeploy(self, service_name: str, tag_new: dict) -> Optional[dict]:
        # Get the service from swarmpit
        service = self.service_get_by_name(service_name)
        if service is None:
            return None

        # Update the service in swarmpit
        headers = {
            "authorization": self.authorization,
            "Content-Type": "application/json; charset=utf-8;"
        }
        r = requests.post(f"{self.url}/services/{service['id']}/redeploy?tag={tag_new}", headers=headers)

        # Success
        if r.status_code == 202:
            return service

        # Not success
        print(f"ERROR - service_redeploy - Status: {r.status_code}, Body: {r.text}")
        return None
