# Table of contents

[[_TOC]]

# Introduction
A tool to be used in CI/CD pipeline job, in which it will update a tag to a Swarmpit service.

# How to use
## Configuration
Example of config.ini
```ini
[swarmpit]
url=https://your.swarmpit.domain
auth=Bearer xxx_api_token_from_admin_of_swarmpit_xxx

[operation]
name=update_service_version
service_name=name_of_the_service_to_be_updated_in_swarmpit
service_repo_name=name of docker image ex: nginx
service_repo_tag=latest
```

## How to run
```bash
python -m swarmpit_client -c config.ini
```