# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
        name="probe_generation_algorithm",
        version="0.0.0",
        description="NetVision Probe Generation",
        author="Zhengzheng Liu",
        license="MIT",
        packages=find_packages(),
        install_requires=['networkx', 'scapy', 'psutil']
    )
