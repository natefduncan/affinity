from setuptools import setup

setup(
        name='affinity',
        version='1.0',
        description='Affinity CRM',
        author='Nathan Duncan',
        author_email='',
        packages=['affinity'],  # would be the same as name
        install_requires=['requests==2.27.1', "dataclasses_json==0.5.7"], #external packages acting as dependencies
        )

