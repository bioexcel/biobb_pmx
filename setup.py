import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_pmx",
    version="3.8.0",
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
    install_requires=['biobb_common==3.8.1'],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "pmxanalyse = biobb_pmx.pmx.pmxanalyse:main",
            "pmxgentop = biobb_pmx.pmx.pmxgentop:main",
            "pmxmutate = biobb_pmx.pmx.pmxmutate:main"
            "pmxatom_mapping = biobb_pmx.pmx.pmxatom_mapping:main",
            "pmxcreate_top = biobb_pmx.pmx.pmxcreate_top:main",
            "pmxligand_hybrid = biobb_pmx.pmx.pmxligand_hybrid:main",
            "pmxmerge_ff = biobb_pmx.pmx.pmxmerge_ff:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
