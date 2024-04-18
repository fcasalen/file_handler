from setuptools import setup, find_packages

setup(
    name='file_handler',
    version='0.1.2',
    license="GNU GENERAL PUBLIC LICENSE",
    author="fcasalen",
    author_email="fcasalen@gmail.com",
    description="package to use handle open and write diverse files as txt, json, xls, etc",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 5 - Prodution/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12"
    ]
)
