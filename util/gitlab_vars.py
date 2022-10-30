import os
from datetime import datetime

import click
import requests
from click import UsageError

# default settings
DEFAULT_GITLAB_URL = "https://gitlab.com/api/v4"
DEFAULT_DATE_TIME_FORMAT = "%Y%m%d%H%M%S"

# Gitalb CI/CD variables
ENV_GITLAB_PROJECT_ID = "CI_PROJECT_ID"
ENV_GITLAB_JOB_TOKEN = "CI_JOB_TOKEN"
ENV_GITLAB_API_URL = "CI_API_V4_URL"

# custom variables
ENV_CUSTOM_TOKEN = "GITLAB_VARS_PERSONAL_TOKEN"
ENV_CUSTOM_PROJECT_ID = "GITLAB_VARS_PROJECT_ID"
ENV_CUSTOM_API_URL = "GITLAB_VARS_API_URL"


def get_token():
    if ENV_CUSTOM_TOKEN in os.environ:
        return "PRIVATE-TOKEN", os.environ[ENV_CUSTOM_TOKEN]
    elif ENV_GITLAB_JOB_TOKEN in os.environ:
        return "JOB-TOKEN", os.environ[ENV_GITLAB_JOB_TOKEN]
    else:
        raise UsageError(f"Token not found. {ENV_CUSTOM_TOKEN} or {ENV_GITLAB_JOB_TOKEN} is not set")


def get_project():
    if ENV_CUSTOM_PROJECT_ID in os.environ:
        return os.environ[ENV_CUSTOM_PROJECT_ID]
    elif ENV_GITLAB_PROJECT_ID in os.environ:
        return os.environ[ENV_GITLAB_PROJECT_ID]
    else:
        return None


def get_base_url():
    if ENV_CUSTOM_API_URL in os.environ:
        return os.environ[ENV_CUSTOM_API_URL]
    elif ENV_GITLAB_API_URL in os.environ:
        return os.environ[ENV_GITLAB_API_URL]
    else:
        return DEFAULT_GITLAB_URL


def get_headers():
    token_type, token = get_token()
    return {token_type: token}


def get_var(project, variable):
    return requests.get(f"{get_base_url()}/projects/{project}/variables/{variable}", headers=get_headers())


def post_var(project, key, value):
    data = {'key': key, 'value': str(value)}
    return requests.post(f"{get_base_url()}/projects/{project}/variables", data=data, headers=get_headers())


def put_var(project, key, value):
    data = {'key': key, 'value': str(value)}
    return requests.put(f"{get_base_url()}/projects/{project}/variables/{key}", data=data, headers=get_headers())


@click.group()
def cli():
    get_token()


@cli.command()
def info():
    toke_type, token = get_token()
    masked = len(token[:-5]) * "*" + token[-5:]
    print(f"TOKEN (masked): {masked}")
    print(f"TOKEN TYPE: {toke_type}")
    print(f"API URL: {get_base_url()}")


@cli.command()
@click.option('--project', default=get_project())
@click.argument('key')
def decr(project, key):
    if project is None:
        raise UsageError("Missing project id")

    resp = get_var(project, key)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")

    val = resp.json()['value']
    try:
        new_val = int(val) - 1
    except ValueError:
        raise UsageError(f"Could not change value '{val}'")
    resp = put_var(project, key, new_val)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")


@cli.command()
@click.option('--project', default=get_project())
@click.argument('key')
def incr(project, key):
    if project is None:
        raise UsageError("Missing project id")

    resp = get_var(project, key)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")

    val = resp.json()['value']
    try:
        new_val = int(val) + 1
    except ValueError:
        raise UsageError(f"Could not change value '{val}'")

    resp = put_var(project, key, new_val)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")


@cli.command()
@click.option('--project', default=get_project())
@click.argument('key')
@click.option('--format', default=DEFAULT_DATE_TIME_FORMAT)
def timestamp(project, key, format):
    if project is None:
        raise UsageError("Missing project id")
    now = datetime.now()
    date_time_str = now.strftime(format)
    resp = put_var(project, key, date_time_str)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")


@cli.command()
@click.option('--project', default=get_project())
@click.argument('key')
def get(project, key):
    if project is None:
        raise UsageError("Missing project id")
    resp = get_var(project, key)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")

    if len(resp.json()) > 0:
        print(resp.json()['value'])
    else:
        raise UsageError(f"Project ({project}) variable ({key}) not set")


@cli.command()
@click.option('--project', default=get_project())
@click.argument('key')
@click.argument('value')
def create(project, key, value):
    if project is None:
        raise UsageError("Missing project id")
    resp = post_var(project, key, value)
    if resp.status_code != 201:
        raise UsageError(f"Got status code {resp.status_code}")


@cli.command()
@click.option('--project', default=get_project())
@click.argument('key')
@click.argument('value')
def update(project, key, value):
    if project is None:
        raise UsageError("Missing project id")
    resp = put_var(project, key, value)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")


if __name__ == '__main__':
    cli()
