import crayons

from jsonschema import ValidationError, validate, FormatChecker
from crab.common import yaml_read


def validate_crabfiles(filename: str, schema: dict = None):
    data = yaml_read(filename)
    if not schema:
        return data
    if not data:
        print(crayons.red(f'No object generated from {filename}'))
        return None
    try:
        validate(instance=data, schema=schema, format_checker=FormatChecker())
    except ValidationError as validation_failed:
        print(crayons.red(f'{filename} invalid: {validation_failed}'))
        return None
    return data
