from setuptools import setup, find_packages

# Setting up
setup(
      # the name must match the folder name 'verysimplemodule'
      name="vizual",
      version="0.0.1",
      author="Hugo Dolan",
      author_email="<hugojdolan@gmail.com>",
      description="Clean visual debugging suite for python",
      long_description="See readme file",
      packages=['vizual'],
      entry_points={
            'console_scripts': [
                  'vizual = vizual.vizual:main',
            ],
      },
      include_package_data=True,
      install_requires=['Flask','requests','docopt'], # add any additional packages that
      # needs to be installed along with your package. Eg: 'caer'
      
      keywords=['python', 'debugging', 'webapp', 'visual'],
      classifiers= [
                    "Development Status :: 1 - Alpha",
                    "Intended Audience :: Developers",
                    "Programming Language :: Python :: 2",
                    "Programming Language :: Python :: 3",
                    "Operating System :: MacOS :: MacOS X",
                    "Operating System :: Microsoft :: Windows",
                    ]
      )