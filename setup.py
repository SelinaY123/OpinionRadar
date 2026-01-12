"""
抖音分析工具的安装配置文件 Installation and configuration file of the Douyin analysis tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="douyin-comment-analyzer",
    version="0.1.0",
    author="SelinaSun",
    author_email="Yue@gmail.com",
    description="抖音评论爬取与分析工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SelinaY123/douyin-comment-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "jieba>=0.42.0",
        "requests>=2.31.0",
        "PyYAML>=6.0",
        "tqdm>=4.65.0",
    ],
    entry_points={
        "console_scripts": [
            "douyin-analyze=src.cli:main",
        ],
    },
)