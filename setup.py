from setuptools import setup

setup(
        name='affinity-crm',
        version='v1.1.7',
        description='Affinity CRM',
        author='Nathan Duncan & Mehmet Oner Yalcin',
        author_email='natefduncan@gmail.com, oneryalcin@gmail.com',
        url="https://github.com/oneryalcin/affinity",
        packages=['affinity', 'affinity.client', 'affinity.common', 'affinity.core'],
        install_requires=['requests>=2.28.0', "dataclasses_json>=0.6.1", "tenacity>=8.2.3"],
        )

