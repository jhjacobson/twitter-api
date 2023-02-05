from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Python package to interact with Twitter API and DC 311 app'
LONG_DESCRIPTION = 'This is a package to interact with the Twitter API and the DC 311 app. This allows you to search over tweets meant to be sent to 311, find the SR, and pull in data about the SR.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="src", 
        version=VERSION,
        author="Josh Jacobson",
        author_email="joshhjacobson@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'DC 311'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Government",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)