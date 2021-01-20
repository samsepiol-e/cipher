from setuptools import setup
from __init__ import *
setup(
    name="credential-tools",
    version="1.0.2",
    description="A GUI tool to manage/encrypt/decrypt your credentials.",
    #long_description=README,
    #long_description_content_type="text/markdown",
    #url="https://github.com/realpython/reader",
    author="Sam Sepiol",
    author_email="0.alicegawa@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    #packages=['lib'],
    #packages=["CredentialTools", 'lib'],
    include_package_data=True,
    install_requires=[
        "pybase64", "pycrypto", "pillow"
    ],
    entry_points={"console_scripts": ["credtools=__main__:main"]},
)
