import os
from datetime import datetime

import click
import requests
from click import UsageError

DEFAULT_GITLAB_URL = "https://gitlab.com/api/v4"
DEFAULT_DATE_TIME_FORMAT = "%Y%m%d%H%M%S"


def get_token():
    if "GITLAB_TOKEN" in os.environ:
        return os.environ["GITLAB_TOKEN"]
    elif "CI_JOB_TOKEN" in os.environ:
        return os.environ["CI_JOB_TOKEN"]
    else:
        raise UsageError("env GITLAB_TOKEN is not set")


def get_base_url():
    if "GITLAB_URL_API" in os.environ:
        return os.environ["GITLAB_URL_API"]
    elif "CI_API_V4_URL" in os.environ:
        return os.environ["CI_API_V4_URL"]
    else:
        return DEFAULT_GITLAB_URL


def get_headers():
    return {"PRIVATE-TOKEN": get_token()}


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
    unmasked = str(get_token)
    masked = len(unmasked[:-5]) * "*" + unmasked[-5:]
    print(f"TOKEN (masked): {masked}")
    print(f"API URL: {get_base_url()}")


@cli.command()
@click.argument('project')
@click.argument('key')
def decr(project, key):
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
@click.argument('project')
@click.argument('key')
def incr(project, key):
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
@click.argument('project')
@click.argument('key')
@click.argument('format', default=DEFAULT_DATE_TIME_FORMAT)
def timestamp(project, key, format):
    now = datetime.now()
    date_time_str = now.strftime(format)
    resp = put_var(project, key, date_time_str)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")


@cli.command()
@click.argument('project')
@click.argument('key')
def get(project, key):
    resp = get_var(project, key)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")

    if len(resp.json()) > 0:
        print(resp.json()['value'])
    else:
        raise UsageError(f"Project ({project}) variable ({key}) not set")


@cli.command()
@click.argument('project')
@click.argument('key')
@click.argument('value')
def create(project, key, value):
    resp = post_var(project, key, value)
    if resp.status_code != 201:
        raise UsageError(f"Got status code {resp.status_code}")


@cli.command()
@click.argument('project')
@click.argument('key')
@click.argument('value')
def update(project, key, value):
    resp = put_var(project, key, value)
    if resp.status_code != 200:
        raise UsageError(f"Got status code {resp.status_code}")


if __name__ == '__main__':
    cli()
