from setuptools import setup

setup(
        name='affinity-crm',
        version='v1.0.2',
        description='Affinity CRM',
        author='Nathan Duncan',
        author_email='natefduncan@gmail.com',
        url="https://github.com/natefduncan/affinity", 
        packages=['affinity', 'affinity.client', 'affinity.common', 'affinity.core'],
        install_requires=['requests==2.27.1', "dataclasses_json==0.5.7"],
        )

