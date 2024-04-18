from setuptools import setup, find_packages

setup(
    name='selench',
    version='19.04.2024',
    packages=find_packages(),
    url='https://github.com/dsymbol/selench',
    license='OSI Approved :: MIT License',
    author='dsymbol',
    description='Selenium wrapper for Python',
    include_package_data=True,
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'selenium==4.19.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
