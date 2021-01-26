import os
import subprocess
import shutil
import crayons
import yaml
import re


def get_home():
    return os.path.expanduser('~')


def get_cwd():
    return os.path.abspath(
        subprocess.check_output('pwd', universal_newlines=True).strip()
    )


def get_crabfile():
    return os.path.join(get_cwd(), '.crab.yml')


def get_crabstate():
    return os.path.join(get_cwd(), '.crabstate.yml')


def get_crabdir():
    return os.path.join(get_cwd(), '.crab')


def yaml_read(filename: str):
    if not os.path.exists(filename):
        print(crayons.red(f'File {filename} does not exist.'))
        return
    with open(filename, mode='r') as yaml_file:
        return yaml.safe_load(yaml_file)


def yaml_write(filename: str, data: dict):
    with open(filename, mode='w') as yaml_file:
        if not data:
            print(crayons.red(f'Trying to write empty data to {filename}'))
            return
        yaml.safe_dump(data, yaml_file)


def activate_azure_env(environment: str = ''):
    if not environment:
        try:
            del os.environ['AZURE_CONFIG_DIR']
        except KeyError:
            pass
        print(crayons.green(f'Azure environment default used.'))
        return

    azure_path = os.path.join(get_home(), f'.azure-{environment}')
    if not os.path.exists(azure_path):
        os.mkdir(azure_path)
        print(crayons.green(f'Azure environment {environment} created on {azure_path}'))

    os.environ['AZURE_CONFIG_DIR'] = azure_path
    print(crayons.green(f'Azure environment {environment} used.'))
    return azure_path


def list_azure_env(crab_data: dict):
    crab_envs = [env.get('name') for env in crab_data['project']['environments']]
    azure_paths = list(filter(lambda path: '.azure' in path, os.listdir(get_home())))
    current = crab_data['project']['current']
    environments = {}

    for path in azure_paths:
        if path == '.azure':
            environment = 'default'
        else:
            environment = path.replace('.azure-', '')
        environments[environment] = {
            'is_crab': environment in crab_envs,
            'is_current': environment == current
        }
    return environments


def destroy_azure_env(environment: str):
    azure_path = os.path.join(get_home(), f'.azure-{environment}')
    try:
        del os.environ['AZURE_CONFIG_DIR']
    except KeyError:
        pass
    print(crayons.green(f'Azure environment {environment} unset.'))
    if not os.path.exists(azure_path):
        return
    shutil.rmtree(azure_path)
    print(crayons.green(f'Azure environment {environment} deleted from {azure_path}.'))


def is_valid_filename(filename: str):
    invalid = re.compile(r'[^0-9a-zA-Z-._]+')
    invalid_chars = invalid.findall(filename)
    return not invalid_chars, invalid_chars


def normalize_filename(filename: str):
    valid, invalid_chars = is_valid_filename(filename)
    if not valid:
        print(crayons.red(f'Filename contains invalid characters {invalid_chars}'))
        return
    return filename.replace('.', '-').replace('_', '-')
