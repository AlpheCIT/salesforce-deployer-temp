from setuptools import setup, find_packages

setup(
    name='salesforce-deployer',
    version='0.1.0',
    description='A tool for deploying Salesforce metadata using a JSON schema configuration.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/salesforce-deployer',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'python-dotenv',
        'requests',
        'click',
        'pytest'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)