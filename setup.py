from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ominicall",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn[standard]>=0.21.0",
        "websockets>=10.0",
        "aiortc>=1.3.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    author="Vamshidhar Reddy Gorre",
    description="A lightweight, headless WebRTC-based communication SDK for 1-on-1 voice calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ominicall",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/ominicall/issues",
        "Documentation": "https://github.com/yourusername/ominicall#readme",
        "Source": "https://github.com/yourusername/ominicall",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Telephony",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    license="MIT",
)