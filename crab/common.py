import os
import subprocess
import shutil
import crayons


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


def activate_azure_env(environment: str):
    azure_path = os.path.join(get_home(), f'.azure-{environment}')
    if not os.path.exists(azure_path):
        os.mkdir(azure_path)
        print(crayons.green(f'Azure environment {environment} created on {azure_path}'))
        return
    os.environ['AZURE_CONFIG_DIR'] = azure_path
    print(crayons.green(f'Azure environment {environment} used.'))


def list_azure_env():
    azure_paths = list(filter(lambda path: '.azure' in path, os.listdir(get_home())))
    current_env_path = os.getenv('AZURE_CONFIG_DIR')
    current_env = current_env_path.split(get_home())[-1].strip(os.sep) if current_env_path else ''
    environments = {}

    for path in azure_paths:
        current = (path == current_env)
        if path == '.azure':
            environment = 'default'
        else:
            environment = path.strip('.azure-')
        environments[environment] = current
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
