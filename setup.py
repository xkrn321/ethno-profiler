from setuptools import setup, find_packages

setup(
    name="ethno-profiler",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25",
        "matplotlib>=3.5",
        "numpy>=1.20",
    ],
    entry_points={
        "console_scripts": [
            "ethno-profiler=ethno_profiler.cli:main",
        ],
    },
    author="许库兰·阿不都许库尔",
    description="Exploratory PubMed publication-count profiling for ethnomedicine research",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
