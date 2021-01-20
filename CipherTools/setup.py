from setuptools import setup
from Cred.__main__ import main
setup(
    name="Cipher Tools",
    version="0.0.2",
    description="Collection of lib and GUI tool for steganography/manage/encrypt/decrypt your credentials.",
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
    packages=["CipherLib"],
    include_package_data=True,
    install_requires=[
        "pybase64", "pycrypto", "pillow"
    ],
    entry_points={"console_scripts": [
        "credtools=Cred.__main__:main",
        "stegtools=Steg.__main__:main"
        ]},
)
