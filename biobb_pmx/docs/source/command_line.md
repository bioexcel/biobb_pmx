# BioBB PMX Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Pmxanalyse
Wrapper class for the PMX analyse module.
### Get help
Command:
```python
pmxanalyse -h
```
    /bin/sh: pmxanalyse: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_a_xvg_zip_path** (*string*): Path the zip file containing the dgdl.xvg files of the A state. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/xvg_A.zip). Accepted formats: ZIP
* **input_b_xvg_zip_path** (*string*): Path the zip file containing the dgdl.xvg files of the B state. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/xvg_B.zip). Accepted formats: ZIP
* **output_result_path** (*string*): Path to the TXT results file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_result.txt). Accepted formats: TXT
* **output_work_plot_path** (*string*): Path to the PNG plot results file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_plot.png). Accepted formats: PNG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **method** (*string*): (CGI BAR JARZ) Choose one or more estimators to use. .
* **temperature** (*number*): (298.15) Temperature in Kelvin..
* **nboots** (*integer*): (0) Number of bootstrap samples to use for the bootstrap estimate of the standard errors..
* **nblocks** (*integer*): (1) Number of blocks to divide the data into for an estimate of the standard error..
* **integ_only** (*boolean*): (False) Whether to do integration only..
* **reverseB** (*boolean*): (False) Whether to reverse the work values for the backward (B->A) transformation..
* **skip** (*integer*): (1) Skip files..
* **slice** (*string*): (None) Subset of trajectories to analyze. Provide list slice, e.g. "10 50" will result in selecting dhdl_files[10:50]..
* **rand** (*integer*): (None) Take a random subset of trajectories. Default is None (do not take random subset)..
* **index** (*string*): (None) Zero-based index of files to analyze (e.g. "0 10 20 50 60"). It keeps the dhdl.xvg files according to their position in the list, sorted according to the filenames..
* **prec** (*integer*): (2) The decimal precision of the screen/file output..
* **units** (*string*): (kJ) The units of the output. .
* **no_ks** (*boolean*): (False) Whether to do a Kolmogorov-Smirnov test to check whether the Gaussian assumption for CGI holds..
* **nbins** (*integer*): (20) Number of histograms bins for the plot..
* **dpi** (*integer*): (300) Resolution of the plot..
* **pmx_path** (*string*): (pmx) Path to the PMX command line interface..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse.yml)
```python
properties:
  dpi: 600
  method: CGI BAR JARZ
  temperature: 298.15

```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_docker.yml)
```python
properties:
  container_image: mmbirb/pmx:1.0
  container_path: docker
  dpi: 600
  method: CGI BAR JARZ
  temperature: 298.15

```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_singularity.yml)
```python
properties:
  container_image: shub://bioexcel/pmx_docker
  container_path: docker
  dpi: 600
  method: CGI BAR JARZ
  temperature: 298.15

```
#### Command line
```python
pmxanalyse --config config_pmxanalyse.yml --input_a_xvg_zip_path xvg_A.zip --input_b_xvg_zip_path xvg_B.zip --output_result_path ref_result.txt --output_work_plot_path ref_plot.png
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse.json)
```python
{
  "properties": {
    "method": "CGI BAR JARZ",
    "temperature": 298.15,
    "dpi": 600
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_docker.json)
```python
{
  "properties": {
    "method": "CGI BAR JARZ",
    "temperature": 298.15,
    "dpi": 600,
    "container_path": "docker",
    "container_image": "mmbirb/pmx:1.0"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_singularity.json)
```python
{
  "properties": {
    "method": "CGI BAR JARZ",
    "temperature": 298.15,
    "dpi": 600,
    "container_path": "docker",
    "container_image": "shub://bioexcel/pmx_docker"
  }
}
```
#### Command line
```python
pmxanalyse --config config_pmxanalyse.json --input_a_xvg_zip_path xvg_A.zip --input_b_xvg_zip_path xvg_B.zip --output_result_path ref_result.txt --output_work_plot_path ref_plot.png
```

## Pmxgentop
Wrapper class for the PMX gentop module.
### Get help
Command:
```python
pmxgentop -h
```
    /bin/sh: pmxgentop: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_zip_path** (*string*): Path the input GROMACS topology TOP and ITP files in zip format. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topology.zip). Accepted formats: ZIP
* **output_top_zip_path** (*string*): Path the output TOP topology in zip format. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_topology.zip). Accepted formats: ZIP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **force_field** (*string*): (amber99sb-star-ildn-mut) Force field to use. If **input_top_zip_path** is a top file, it's not necessary to specify the forcefield, as it will be determined automatically. If **input_top_zip_path** is an itp file, then it's needed..
* **split** (*boolean*): (False) Write separate topologies for the vdW and charge transformations..
* **scale_mass** (*boolean*): (False) Scale the masses of morphing atoms so that dummies have a mass of 1..
* **gmx_lib** (*string*): ($CONDA_PREFIX/lib/python3.7/site-packages/pmx/data/mutff45/) Path to the GMXLIB folder in your computer..
* **pmx_path** (*string*): (pmx) Path to the PMX command line interface..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/inout) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop.yml)
```python
properties:
  force_field: amber99sb-star-ildn-mut

```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_docker.yml)
```python
properties:
  container_image: mmbirb/pmx:1.0
  container_path: docker
  force_field: amber99sb-star-ildn-mut

```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_singularity.yml)
```python
properties:
  container_image: shub://bioexcel/pmx_docker
  container_path: docker
  force_field: amber99sb-star-ildn-mut

```
#### Command line
```python
pmxgentop --config config_pmxgentop.yml --input_top_zip_path topology.zip --output_top_zip_path ref_output_topology.zip
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop.json)
```python
{
  "properties": {
    "force_field": "amber99sb-star-ildn-mut"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_docker.json)
```python
{
  "properties": {
    "force_field": "amber99sb-star-ildn-mut",
    "container_path": "docker",
    "container_image": "mmbirb/pmx:1.0"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_singularity.json)
```python
{
  "properties": {
    "force_field": "amber99sb-star-ildn-mut",
    "container_path": "docker",
    "container_image": "shub://bioexcel/pmx_docker"
  }
}
```
#### Command line
```python
pmxgentop --config config_pmxgentop.json --input_top_zip_path topology.zip --output_top_zip_path ref_output_topology.zip
```

## Pmxmutate
Wrapper class for the PMX mutate module.
### Get help
Command:
```python
pmxmutate -h
```
    /bin/sh: pmxmutate: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Path to the input structure file. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/frame99.pdb). Accepted formats: PDB, GRO
* **output_structure_path** (*string*): Path to the output structure file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_structure.pdb). Accepted formats: PDB, GRO
* **input_b_structure_path** (*string*): Path to the mutated input structure file. File type: input. [Sample file](None). Accepted formats: PDB, GRO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mutation_list** (*string*): (2Ala) Mutation list in the format "Chain:Resnum MUT_AA_Code" or "Chain:Resnum MUT_NA_Code"  (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:15CYS". Possible MUT_AA_Code: 'ALA', 'ARG', 'ASN', 'ASP', 'ASPH', 'ASPP', 'ASH', 'CYS', 'CYS2', 'CYN', 'CYX', 'CYM', 'CYSH', 'GLU', 'GLUH', 'GLUP', 'GLH', 'GLN', 'GLY', 'HIS', 'HIE', 'HISE', 'HSE', 'HIP', 'HSP', 'HISH', 'HID', 'HSD', 'ILE', 'LEU', 'LYS', 'LYSH', 'LYP', 'LYN', 'LSN', 'MET', 'PHE', 'PRO', 'SER', 'SP1', 'SP2', 'THR', 'TRP', 'TYR', 'VAL'. Possible MUT_NA_Codes: 'A', 'T', 'C', 'G', 'U'..
* **force_field** (*string*): (amber99sb-star-ildn-mut) Forcefield to use..
* **resinfo** (*boolean*): (False) Show the list of 3-letter -> 1-letter residues..
* **gmx_lib** (*string*): ($CONDA_PREFIX/lib/python3.7/site-packages/pmx/data/mutff45/) Path to the GMXLIB folder in your computer..
* **pmx_path** (*string*): (pmx) Path to the PMX command line interface..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/inout) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate.yml)
```python
properties:
  force_field: amber99sb-star-ildn-mut
  mutation_list: 2Ala, 3Val

```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_docker.yml)
```python
properties:
  container_image: quay.io/biocontainers/pmx_biobb:1.0.0--py37h9d97f00_1
  container_path: docker
  force_field: amber99sb-star-ildn-mut
  mutation_list: 2Ala, 3Val

```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_singularity.yml)
```python
properties:
  container_image: shub://bioexcel/pmx_docker
  container_path: singularity
  force_field: amber99sb-star-ildn-mut
  mutation_list: 2Ala, 3Val

```
#### Command line
```python
pmxmutate --config config_pmxmutate.yml --input_structure_path frame99.pdb --output_structure_path ref_output_structure.pdb --input_b_structure_path input.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate.json)
```python
{
  "properties": {
    "mutation_list": "2Ala, 3Val",
    "force_field": "amber99sb-star-ildn-mut"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_docker.json)
```python
{
  "properties": {
    "mutation_list": "2Ala, 3Val",
    "force_field": "amber99sb-star-ildn-mut",
    "container_path": "docker",
    "container_image": "quay.io/biocontainers/pmx_biobb:1.0.0--py37h9d97f00_1"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_singularity.json)
```python
{
  "properties": {
    "mutation_list": "2Ala, 3Val",
    "force_field": "amber99sb-star-ildn-mut",
    "container_path": "singularity",
    "container_image": "shub://bioexcel/pmx_docker"
  }
}
```
#### Command line
```python
pmxmutate --config config_pmxmutate.json --input_structure_path frame99.pdb --output_structure_path ref_output_structure.pdb --input_b_structure_path input.pdb
```
