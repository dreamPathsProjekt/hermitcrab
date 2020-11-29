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


@click.group()
def cli():
    pass


@cli.command(help='')
@click.option('--force', '-f', is_flag=True, default=False, type=click.BOOL, help='Overwrite existing configuration')
def init(force):
    project_name = input(crayons.yellow('Project name: '))
    env_name = input(crayons.yellow('Default environment name: '))
    vault_name = input(crayons.yellow('Default Azure KeyVault name: '))
    if not project_name or not env_name or vault_name:
        print(crayons.red('Empty values not allowed.'))
        return

    azure_path = activate_azure_env(env_name)
    init_data = {
        'project': {
            'name': project_name,
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
        print(crayons.red(f'Crabfile {crabfile} already exists. Exiting.'))
        return
    if os.path.exists(crab_state) and not force:
        print(crayons.red(f'Crab statefile {crab_state} already exists. Exiting.'))
        return

    yaml_write(crabfile, init_data)
    print(crayons.green(f'Crabfile {crabfile} initialized.'))
    yaml_write(crab_state, init_data)
    print(crayons.green(f'Crab statefile {crab_state} initialized.'))
    VaultClient.get_client(vault_name)
    print(crayons.green(f'Azure KeyVault {vault_name} set for project {project_name}'))
