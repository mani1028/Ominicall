from setuptools import setup, find_packages

setup(
    name="ominicall",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "websockets",
        "aiortc",
        "aiohttp"
    ],
    author="Vamshidhar Reddy Gorre",
    description="A real-time WebRTC-based communication SDK",
    python_requires=">=3.8",
)