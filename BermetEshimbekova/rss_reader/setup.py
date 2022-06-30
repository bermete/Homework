from setuptools import setup, find_packages
import rss_reader
from rss_reader import __version__

with open('requirements.txt') as f:
	requirements = f.readlines()

description='RSS Parser',

setup(
		name ='rss_reader',
		version =__version__,
		author ='Bermet Eshimbekova ',
		author_email ='beshimbekova@gmail.com',
		url ='https://github.com/bermete/Homework/tree/final_task',
		description ='Final task. RSS reader',
		long_description = description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
        include_package_data=True,
        install_requires = requirements,
		entry_points ={
			'console_scripts': ['rss_reader = rss_reader.rss_reader:rss_reader']
		},
		classifiers =(
			"Programming Language :: Python :: 3.10",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='rss',
		zip_safe = False
)
