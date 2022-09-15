# Biobb PMX changelog

## What's new in version [3.8.0](https://github.com/bioexcel/biobb_pmx/releases/tag/v3.8.0)?
In version 3.8.0 the dependency biobb_common has been updated to 3.8.1 version.
Three new modules have been added

### New features

* Update to biobb_common 3.8.0 (general)
* Three new modules have been added

## What's new in version [3.7.0](https://github.com/bioexcel/biobb_pmx/releases/tag/v3.7.0)?
In version 3.7.0 the dependency biobb_common has been updated to 3.7.0 version.

### New features

* Update to biobb_common 3.7.0 (general)

## What's new in version [3.6.0](https://github.com/bioexcel/biobb_pmx/releases/tag/v3.5.0)?
In version 3.0.3 the dependency biobb_common has been updated to 3.5.1 version. Also, there has been implemented the new version of docstrings, therefore the JSON Schemas have been modified.

### New features

* Update to biobb_common 3.6.0 (general)
* Update to Biopython 1.79 (general)
* New extended and improved JSON schemas (Galaxy and CWL-compliant) (general)

### Other changes

* New docstrings

## What's new in version [3.6.0](https://github.com/bioexcel/biobb_pmx/releases/tag/v3.6.0)?
In version 3.6.0 PMX software has been updated to its python 3 version and thus, biobb_pmx breaks its dependence from docker.

### New features

* First full python 3 compatible version of biobb_pmx

## What's new in version [3.6.0](https://github.com/bioexcel/biobb_pmx/releases/tag/v3.6.0)?
In version 3.6.0 Python has been updated to version 3.7 and Biopython to version 1.79.
Big changes in the documentation style and content. Finally a new conda installation recipe has been introduced.

### New features

* Update to Python 3.7 (general)
* Update to Biopython 1.79 (general)
* New conda installer (installation)
* Adding type hinting for easier usage (API)
* Deprecating os.path in favour of pathlib.path (modules)
* New command line documentation (documentation)

### Bug fixes

* Replace container Quay.io badge (documentation)
* Remove unused system and step arguments from command line causing execution errors (cli) [#9](https://github.com/bioexcel/biobb_model/issues/9)
* Replace wrong arguments in pmxgentop.py commandline (commandline)

### Other changes

* New documentation styles (documentation) [#8](https://github.com/bioexcel/biobb_model/issues/8)
