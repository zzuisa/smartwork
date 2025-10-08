#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("confs/requrements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="smartwork",
    version="1.5.0",
    author="SmartWork Team",
    author_email="smartwork@example.com",
    description="智能工作日志管理系统 - 自动生成每日工作文件夹和月底交付件报表",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/zzuisa/smartwork",
    project_urls={
        "Bug Reports": "https://github.com/zzuisa/smartwork/issues",
        "Source": "https://github.com/zzuisa/smartwork",
        "Documentation": "https://github.com/zzuisa/smartwork#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "flake8>=3.8",
            "black>=21.0",
            "isort>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smartwork=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["confs/*.ini", "confs/*.txt"],
    },
    keywords="worklog, excel, automation, productivity, office, business",
    zip_safe=False,
)
