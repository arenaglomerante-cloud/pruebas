"""Setup configuration for GEX Quant Analysis Platform"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gex-quant-analysis",
    version="0.1.0",
    author="Arena Glomerante Cloud",
    author_email="contact@arenagc.com",
    description="Gamma Exposure (GEX) analysis platform for NQ and NDX markets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arenaglomerante-cloud/pruebas",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "pylint>=2.17.0",
            "jupyter>=1.0.0",
        ],
    },
)
