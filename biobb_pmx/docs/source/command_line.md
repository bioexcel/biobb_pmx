# BioBB PMX Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Pmxanalyse
Wrapper class for the [PMX analyse](https://github.com/deGrootLab/pmx) module.
### Get help
Command:
```python
pmxanalyse -h
```
    /bin/sh: pmxanalyse: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_a_xvg_zip_path** (*string*): Path the zip file containing the dgdl. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/xvg_A.zip). Accepted formats: ZIP
* **input_b_xvg_zip_path** (*string*): Path the zip file containing the dgdl. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/xvg_B.zip). Accepted formats: ZIP
* **output_result_path** (*string*): Path to the TXT results file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_result.txt). Accepted formats: TXT
* **output_work_plot_path** (*string*): Path to the PNG plot results file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_plot.png). Accepted formats: PNG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **method** (*string*): (CGI BAR JARZ) Choose one or more estimators to use from the available ones: CGI, BAR, JARZ..
* **temperature** (*float*): (298.15) Temperature in Kelvin..
* **nboots** (*number*): (0) Number of bootstrap samples..
* **nblocks** (*number*): (1) Number of blocks to divide the data into for an estimate of the standard error..
* **integ_only** (*boolean*): (False) Whether to do integration only..
* **reverseB** (*boolean*): (False) transformation..
* **skip** (*number*): (1) Skip files..
* **slice** (*number*): (All) Subset of trajectories to analyze..
* **index** (*boolean*): (All) Zero-based index of files to analyze..
* **prec** (*number*): (2) The decimal precision of the screen/file output..
* **units** (*string*): (KJ) The units of the output. Choose from "kJ", "kcal", "kT"..
* **no_ks** (*boolean*): (False) Whether to do a Kolmogorov-Smirnov test to check whether the Gaussian assumption for CGI holds..
* **nbins** (*number*): (10) Number of histograms bins for the plot..
* **dpi** (*number*): (300) Resolution of the plot..
* **pmx_cli_path** (*string*): (cli.py) Path to the PMX Python2.7 client..
* **remove_tmp** (*boolean*): (True) [WF property] Remove temporal files..
* **restart** (*boolean*): (False) [WF property] Do not execute if output files exist..
* **container_path** (*string*): (None)  Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse.yml)
```python
properties:
  pmx_cli_path: /Users/pau/other_projects/pmx/pmx/scripts/cli.py

```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_docker.yml)
```python
properties:
  container_image: mmbirb/pmx
  container_path: docker

```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_singularity.yml)
```python
properties:
  container_image: shub://bioexcel/pmx_docker
  container_path: docker

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
    "pmx_cli_path": "/Users/pau/other_projects/pmx/pmx/scripts/cli.py"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "mmbirb/pmx"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxanalyse_singularity.json)
```python
{
  "properties": {
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
Wrapper class for the [PMX gentop](https://github.com/deGrootLab/pmx) module.
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
* **force_field** (*string*): (amber99sb-star-ildn-mut) Forcefield..
* **split** (*boolean*): (False) Print a 3 to 1 letter residue list..
* **scale_mass** (*boolean*): (False) Scale mass..
* **dna** (*boolean*): (False) Generate hybrid residue for the DNA nucleotides..
* **rna** (*boolean*): (False) Generate hybrid residue for the RNA nucleotides..
* **output_top_name** (*string*): (gentop.top) Name of the output top file..
* **keyword_list** (*string*): (['Protein', 'DNA']) List of comma separated Keywords to match top and itp files..
* **pmx_cli_path** (*string*): (cli.py) Path to the PMX Python2.7 client..
* **remove_tmp** (*boolean*): (True) [WF property] Remove temporal files..
* **restart** (*boolean*): (False) [WF property] Do not execute if output files exist..
* **container_path** (*string*): (None)  Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/inout) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop.yml)
```python
properties:
  force_field: amber99sbmut
  gmxlib: /Users/pau/other_projects/pmx/pmx/data/mutff45
  pmx_cli_path: /Users/pau/other_projects/pmx/pmx/scripts/cli.py

```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_docker.yml)
```python
properties:
  container_image: mmbirb/pmx
  container_path: docker
  force_field: amber99sbmut

```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_singularity.yml)
```python
properties:
  container_image: shub://bioexcel/pmx_docker
  container_path: docker
  force_field: amber99sbmut

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
    "gmxlib": "/Users/pau/other_projects/pmx/pmx/data/mutff45",
    "force_field": "amber99sbmut",
    "pmx_cli_path": "/Users/pau/other_projects/pmx/pmx/scripts/cli.py"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_docker.json)
```python
{
  "properties": {
    "force_field": "amber99sbmut",
    "container_path": "docker",
    "container_image": "mmbirb/pmx"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxgentop_singularity.json)
```python
{
  "properties": {
    "force_field": "amber99sbmut",
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
Wrapper class for the [PMX mutate](https://github.com/deGrootLab/pmx) module.
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
* **mutation_list** (*string*): (Val2Ala) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:ALA15CYS".
* **force_field** (*string*): (amber99sb-star-ildn-mut) Forcefield..
* **resinfo** (*boolean*): (False) Print a 3 to 1 letter residue list..
* **dna** (*boolean*): (False) Generate hybrid residue for the DNA nucleotides..
* **rna** (*boolean*): (False) Generate hybrid residue for the RNA nucleotides..
* **pmx_cli_path** (*string*): (cli.py) Path to the PMX Python2.7 client..
* **remove_tmp** (*boolean*): (True) [WF property] Remove temporal files..
* **restart** (*boolean*): (False) [WF property] Do not execute if output files exist..
* **container_path** (*string*): (None)  Path to the binary executable of your container..
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
  gmxlib: /Users/pau/other_projects/pmx/pmx/data/mutff45
  mutation_list: Val2Ala, Ile3Val
  pmx_cli_path: /Users/pau/other_projects/pmx/pmx/scripts/cli.py

```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_docker.yml)
```python
properties:
  container_image: mmbirb/pmx
  container_path: docker
  force_field: amber99sb-star-ildn-mut
  mutation_list: Val2Ala, Ile3Val

```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_singularity.yml)
```python
properties:
  container_image: shub://bioexcel/pmx_docker
  container_path: singularity
  force_field: amber99sb-star-ildn-mut
  mutation_list: Val2Ala, Ile3Val

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
    "mutation_list": "Val2Ala, Ile3Val",
    "gmxlib": "/Users/pau/other_projects/pmx/pmx/data/mutff45",
    "force_field": "amber99sb-star-ildn-mut",
    "pmx_cli_path": "/Users/pau/other_projects/pmx/pmx/scripts/cli.py"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_docker.json)
```python
{
  "properties": {
    "mutation_list": "Val2Ala, Ile3Val",
    "force_field": "amber99sb-star-ildn-mut",
    "container_path": "docker",
    "container_image": "mmbirb/pmx"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmutate_singularity.json)
```python
{
  "properties": {
    "mutation_list": "Val2Ala, Ile3Val",
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
