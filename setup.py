import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_pmx",
    version="4.1.0",
    author="Biobb developers",
    author_email="pau.andrio@bsc.es",
    description="Biobb_pmx is the Biobb module collection to perform PMX (http://pmx.mpibpc.mpg.de) executions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_pmx",
    project_urls={
        "Documentation": "http://biobb_pmx.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs']),
    install_requires=['biobb_common==4.1.0', 'pmx-biobb==4.1.3'],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "pmxanalyse = biobb_pmx.pmxbiobb.pmxanalyse:main",
            "pmxgentop = biobb_pmx.pmxbiobb.pmxgentop:main",
            "pmxmutate = biobb_pmx.pmxbiobb.pmxmutate:main",
            "pmxatom_mapping = biobb_pmx.pmxbiobb.pmxatom_mapping:main",
            "pmxcreate_top = biobb_pmx.pmxbiobb.pmxcreate_top:main",
            "pmxligand_hybrid = biobb_pmx.pmxbiobb.pmxligand_hybrid:main",
            "pmxmerge_ff = biobb_pmx.pmxbiobb.pmxmerge_ff:main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix"
    ],
)
