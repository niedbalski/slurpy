from setuptools import setup, find_packages

dependencies = [ "tornado" ]

setup(
    name="slurpy",
    version="0.1",
    packages=find_packages(),
    install_requires=dependencies,
    author="Jorge Niedbalski R.",
    author_email="jnr@pyrosome.org",
    description="Call python methods from javascript and viceversa",
    include_package_data=True,
    license="BSD"
)
