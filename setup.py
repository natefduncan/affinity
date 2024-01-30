from setuptools import setup

setup(
        name='affinity-crm',
        version='v1.1.4',
        description='Affinity CRM',
        author='Nathan Duncan',
        author_email='natefduncan@gmail.com',
        url="https://github.com/natefduncan/affinity", 
        packages=['affinity', 'affinity.client', 'affinity.common', 'affinity.core'],
        install_requires=['requests>=2.28.0', "dataclasses_json>=0.6.1"],
        )

