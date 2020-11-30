import click
import crayons
import os
import shutil

from crab.initialize import VaultClient
from crab.common import (
    activate_azure_env,
    list_azure_env,
    destroy_azure_env,
    yaml_read,
    yaml_write,
    get_crabdir,
    get_crabfile,
    get_crabstate
)


def _is_project_init():
    crab_dir = get_crabdir()
    crabfile = get_crabfile()
    crab_state = get_crabstate()
    crab_data = yaml_read(crabfile)
    crab_state_data = yaml_read(crab_state)
    return (
        crab_data and crab_state_data and os.path.exists(crab_dir),
        crab_data,
        crab_state_data
    )


@click.group()
def cli():
    pass


@cli.group()
def environment():
    pass


@cli.command(help='Initialize Project')
@click.option('--force', '-f', is_flag=True, default=False, type=click.BOOL, help='Overwrite existing configuration')
def init(force):
    project_name = click.prompt(crayons.yellow('Project name'), type=click.STRING)
    env_name = click.prompt(crayons.yellow('Default environment name'), type=click.STRING)
    vault_name = click.prompt(crayons.yellow('Default Azure KeyVault name'), type=click.STRING)
    print(project_name)
    print(env_name)
    print(vault_name)
    if not project_name or not env_name or not vault_name:
        click.echo(crayons.red('Empty values not allowed.'))
        return

    azure_path = activate_azure_env(env_name)
    init_data = {
        'project': {
            'name': project_name,
            'current': env_name,
            'environments': [
                {
                    'name': env_name,
                    'vault': vault_name,
                    'azure_environment': azure_path,
                    'items': []
                }
            ]
        }
    }

    crab_dir = get_crabdir()
    crabfile = get_crabfile()
    crab_state = get_crabstate()
    if force:
        shutil.rmtree(crab_dir)
    if not os.path.exists(crab_dir):
        os.mkdir(crab_dir)
    if os.path.exists(crabfile) and not force:
        click.echo(crayons.red(f'Crabfile {crabfile} already exists. Exiting.'))
        return
    if os.path.exists(crab_state) and not force:
        click.echo(crayons.red(f'Crab statefile {crab_state} already exists. Exiting.'))
        return

    yaml_write(crabfile, init_data)
    click.echo(crayons.green(f'Crabfile {crabfile} initialized.'))
    yaml_write(crab_state, init_data)
    click.echo(crayons.green(f'Crab statefile {crab_state} initialized.'))
    VaultClient.get_client(vault_name)
    click.echo(crayons.green(f'Azure KeyVault {vault_name} set for project {project_name}'))


@environment.command(help='Add an Azure environment')
@click.argument('environment', type=click.STRING)
def add(environment):
    crabfile = get_crabfile()
    crab_state = get_crabstate()
    project_exists, crab_data, crab_state_data = _is_project_init()
    if not project_exists:
        click.echo(crayons.red('Please setup project first using "crab init"'))
        return

    environments = list_azure_env(crab_data)
    for env, state in environments.items():
        if environment == env and state.get('is_crab'):
            click.echo(crayons.red(f'Environment {environment} already exists.'))
            return
    vault_name = click.prompt(crayons.yellow(f'Azure KeyVault name for {environment}'), type=click.STRING)
    azure_path = activate_azure_env(environment)

    new_environ_data = {
        'name': environment,
        'vault': vault_name,
        'azure_environment': azure_path,
        'items': []
    }
    crab_data['project']['environments'].append(new_environ_data)
    crab_state_data['project']['environments'].append(new_environ_data)
    yaml_write(crabfile, crab_data)
    yaml_write(crab_state, crab_state_data)

    VaultClient.get_client(vault_name)
    click.echo(crayons.green(f'Azure KeyVault {vault_name} set for environment {environment}'))


@environment.command(help='Use an Azure environment')
@click.argument('environment', type=click.STRING)
def use(environment):
    crabfile = get_crabfile()
    crab_state = get_crabstate()
    project_exists, crab_data, crab_state_data = _is_project_init()
    if not project_exists:
        click.echo(crayons.red('Please setup project first using "crab init"'))
        return

    common_message = f' Consider using "crab environment add {environment}"'
    environments = list_azure_env(crab_data)
    if environment not in environments.keys():
        click.echo(crayons.red(f'Environment {environment} does not exist.{common_message}'))
        return
    for env, state in environments.items():
        if environment == env and not state.get('is_crab'):
            click.echo(crayons.red(f'Environment {environment} is not a crab environment.{common_message}'))
            return

    crab_data['project']['current'] = environment
    crab_state_data['project']['current'] = environment
    yaml_write(crabfile, crab_data)
    yaml_write(crab_state, crab_state_data)
    click.echo(crayons.green(f'Active environment: {environment}'))


@environment.command(help='List all setup Azure environments.')
def list():
    project_exists, crab_data, crab_state_data = _is_project_init()
    if not project_exists:
        click.echo(crayons.red('Please setup project first using "crab init"'))
        return

    environments = list_azure_env(crab_data)
    for env, state in environments.items():
        is_crab = state.get('is_crab')
        is_current = state.get('is_current')
        suffix = ''
        prefix = ''
        color = crayons.white
        if is_crab:
            prefix = '(crab) '
        if is_current:
            prefix = '(crab) '
            suffix = ' (*)'
            color = crayons.green
        click.echo(color(f'{prefix}{env}{suffix}'))