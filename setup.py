from setuptools import setup, find_packages
from crab import VERSION


setup(
    name="crab",
    version=VERSION,
    author="DreamPathsProjekt",
    url="https://github.com/dreamPathsProjekt/hermitcrab",
    packages=find_packages(),
    include_package_data=True,
    package_dir={'crab': 'crab'},
    package_data={'crab': []},
    python_requires='>=3.6, <4',
    install_requires=[
        "azure-identity ==1.5.0",
        "azure-keyvault-secrets ==4.2.0",
        "click ==7.1.2",
        "crayons ==0.4.0",
        "jsonschema ==3.2.0",
        "PyYAML ==5.3.1",
    ],
    entry_points="""
    [console_scripts]
    crab=crab.cli:cli
    """,
)
