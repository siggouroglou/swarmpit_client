# Introduction
A tool to be used in CI/CD pipeline jobs, in which it will update a tag to a Swarmpit service.

# The tool
## Configuration
Example of config.ini
```ini
[swarmpit]
url=https://your.swarmpit.domain
auth=Bearer xxx_api_token_from_admin_of_swarmpit_xxx

[operation]
name=update_service_version
service_name=name_of_the_service_to_be_updated_in_swarmpit
service_repo_name=name of docker image to be set for the specific service, ex: nginx
service_repo_tag=tag of docker image to be set, ex: latest
```

## How to run
```bash
pip3 install -r requirements.txt
python -m swarmpit_client -c config.ini
```

# For developers

## Module architecture
cli_run -> operations -> api_client

## Git

This project uses `git` version control system and
[Git Flow workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).  
Basically, there are two branches in use, `master` and `develop`.  
Branch `master` contains the production version of the tool, while `develop` branch contains the work in progress.  
If more developers work on this project, it is a good practice to create a branch per feature/work in progress,
on top of the `develop` branch.
