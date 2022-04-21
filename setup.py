from setuptools import setup, find_namespace_packages


setup( 
    name = "remake",
    version = "0.0.1",
    packages = find_namespace_packages(),
    install_requires = [
        'stanza'
    ]
)
