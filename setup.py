from setuptools import setup, find_packages

setup(
    name="netcdf-resilience",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.20.0',
        'xarray>=0.16.0',
        'netCDF4>=1.5.0',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for calculating resilience and reliability metrics from NetCDF timeseries data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/netcdf-resilience",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 