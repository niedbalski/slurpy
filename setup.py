from setuptools import setup, find_packages

dependencies = [ "tornado" ]

setup(
    name="slurpy",
    version="0.1.3",
    packages=find_packages(),
    install_requires=dependencies,
    author="Jorge Niedbalski R.",
    author_email="jnr@pyrosome.org",
    description="Call python methods from javascript and viceversa",
    keywords="rpc javascript js-rpc javascript-rpc call python from javascript slurpy slurpe slurp",
    include_package_data=True,
    license="BSD",
    classifiers=['Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Operating System :: Unix ']
)
