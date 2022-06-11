from setuptools import setup

setup(
        name='affinity-crm',
        version='v1.0.0',
        description='Affinity CRM',
        author='Nathan Duncan',
        author_email='natefduncan@gmail.com',
        url="https://github.com/natefduncan/affinity/archive/refs/tags/v1.0.0.tar.gz", 
        packages=['affinity'],
        install_requires=['requests==2.27.1', "dataclasses_json==0.5.7"],
        )

