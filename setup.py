import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cyberpower_pdu_snmp",
    version="0.0.1",
    author="Brendan Jackman",
    author_email="brendan.jackman@bluwirelesstechnology.com",
    description="Turn stuff on and off with CyberPower PDUs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bjackman/cyberpower_pdu_snmp",
    packages=setuptools.find_packages(),
    install_requires=["pysnmp"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
