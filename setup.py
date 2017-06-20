from setuptools import setup

setup(
    name='benchmarks_server',
    packages=['benchmarks_server'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors',
    ],
)
