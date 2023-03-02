# BioBB PMX Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Pmxligand_hybrid
Wrapper class for the PMX ligand_hybrid module.
### Get help
Command:
```python
pmxligand_hybrid -h
```
    usage: pmxligand_hybrid [-h] [-c CONFIG] --input_structure1_path INPUT_STRUCTURE1_PATH --input_structure2_path INPUT_STRUCTURE2_PATH --input_topology1_path INPUT_TOPOLOGY1_PATH --input_topology2_path INPUT_TOPOLOGY2_PATH --output_structure1_path OUTPUT_STRUCTURE1_PATH --output_structure2_path OUTPUT_STRUCTURE2_PATH --output_topology1_path OUTPUT_TOPOLOGY1_PATH --output_topology2_path OUTPUT_TOPOLOGY2_PATH --output_log_path OUTPUT_LOG_PATH [--input_scaffold1_path INPUT_SCAFFOLD1_PATH] [--input_scaffold2_path INPUT_SCAFFOLD2_PATH] [--input_pairs_path INPUT_PAIRS_PATH]
    
    Run PMX ligand hybrid module
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
      --input_scaffold1_path INPUT_SCAFFOLD1_PATH
                            Path to the index of atoms to consider for the ligand structure 1
      --input_scaffold2_path INPUT_SCAFFOLD2_PATH
                            Path to the index of atoms to consider for the ligand structure 2
      --input_pairs_path INPUT_PAIRS_PATH
                            Path to the input atom pair mapping.
    
    required arguments:
      --input_structure1_path INPUT_STRUCTURE1_PATH
                            Path to the input ligand structure file 1
      --input_structure2_path INPUT_STRUCTURE2_PATH
                            Path to the input ligand structure file 2
      --input_topology1_path INPUT_TOPOLOGY1_PATH
                            Path to the input ligand topology file 1
      --input_topology2_path INPUT_TOPOLOGY2_PATH
                            Path to the input ligand topology file 2
      --output_structure1_path OUTPUT_STRUCTURE1_PATH
                            Path to the output ligand structure file 1
      --output_structure2_path OUTPUT_STRUCTURE2_PATH
                            Path to the output ligand structure file 2
      --output_topology1_path OUTPUT_TOPOLOGY1_PATH
                            Path to the output ligand topology file 1
      --output_topology2_path OUTPUT_TOPOLOGY2_PATH
                            Path to the output ligand topology file 2
      --output_log_path OUTPUT_LOG_PATH
                            Path to the log file
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure1_path** (*string*): Path to the input ligand structure file 1. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb). Accepted formats: PDB
* **input_structure2_path** (*string*): Path to the input ligand structure file 2. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb). Accepted formats: PDB
* **input_topology1_path** (*string*): Path to the input ligand topology file 1. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp). Accepted formats: ITP
* **input_topology2_path** (*string*): Path to the input ligand topology file 2. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp). Accepted formats: ITP
* **input_pairs_path** (*string*): Path to the input atom pair mapping. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_mapping_pairs.dat). Accepted formats: DAT, TXT
* **input_scaffold1_path** (*string*): Path to the index of atoms to consider for the ligand structure 1. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx). Accepted formats: NDX
* **input_scaffold2_path** (*string*): Path to the index of atoms to consider for the ligand structure 2. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx). Accepted formats: NDX
* **output_log_path** (*string*): Path to the log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atom_mapping.log). Accepted formats: LOG, TXT, OUT
* **output_structure1_path** (*string*): Path to the output hybrid structure based on the ligand 1. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb). Accepted formats: PDB
* **output_structure2_path** (*string*): Path to the output hybrid structure based on the ligand 2. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb). Accepted formats: PDB
* **output_topology_path** (*string*): Path to the output hybrid topology. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ligand_hybrid.itp). Accepted formats: ITP
* **output_atomtypes_path** (*string*): Path to the atom types for the output hybrid topology. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ligand_hybrid_atomtypes.itp). Accepted formats: ITP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **fit** (*boolean*): (False) Fit ligand structure 1 onto ligand structure 2 (Only used if input_pairs_path is provided)..
* **split** (*boolean*): (False) Split the topology into separate transitions..
* **scDUMm** (*number*): (1.0) Scale dummy masses using the counterpart atoms..
* **scDUMa** (*number*): (1.0) Scale bonded dummy angle parameters..
* **scDUMd** (*number*): (1.0) Scale bonded dummy dihedral parameters..
* **deAng** (*boolean*): (False) Decouple angles composed of 1 dummy and 2 non-dummies..
* **distance** (*number*): (0.05) Distance (nm) between atoms to consider them morphable for alignment approach (Only used if input_pairs_path is not provided)..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (None) Container Image identifier..
* **container_volume_path** (*string*): (/inout) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxligand_hybrid.yml)
```python
properties:
  distance: 0.05
  fit: true

```
#### Command line
```python
pmxligand_hybrid --config config_pmxligand_hybrid.yml --input_structure1_path ligand.pdb --input_structure2_path ligand.pdb --input_topology1_path ligand.itp --input_topology2_path ligand.itp --input_pairs_path ref_mapping_pairs.dat --input_scaffold1_path atoms_to_consider.ndx --input_scaffold2_path atoms_to_consider.ndx --output_log_path atom_mapping.log --output_structure1_path superimposed_ligand.pdb --output_structure2_path superimposed_ligand.pdb --output_topology_path ligand_hybrid.itp --output_atomtypes_path ligand_hybrid_atomtypes.itp
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxligand_hybrid.json)
```python
{
  "properties": {
    "fit": true,
    "distance": 0.05
  }
}
```
#### Command line
```python
pmxligand_hybrid --config config_pmxligand_hybrid.json --input_structure1_path ligand.pdb --input_structure2_path ligand.pdb --input_topology1_path ligand.itp --input_topology2_path ligand.itp --input_pairs_path ref_mapping_pairs.dat --input_scaffold1_path atoms_to_consider.ndx --input_scaffold2_path atoms_to_consider.ndx --output_log_path atom_mapping.log --output_structure1_path superimposed_ligand.pdb --output_structure2_path superimposed_ligand.pdb --output_topology_path ligand_hybrid.itp --output_atomtypes_path ligand_hybrid_atomtypes.itp
```

## Pmxanalyse
Wrapper class for the PMX analyse module.
### Get help
Command:
```python
pmxanalyse -h
```
    usage: pmxanalyse [-h] [-c CONFIG] --input_a_xvg_zip_path INPUT_A_XVG_ZIP_PATH --input_b_xvg_zip_path INPUT_B_XVG_ZIP_PATH --output_result_path OUTPUT_RESULT_PATH --output_work_plot_path OUTPUT_WORK_PLOT_PATH
    
    Wrapper class for the PMX analyse module.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      --input_a_xvg_zip_path INPUT_A_XVG_ZIP_PATH
                            Path the zip file containing the dgdl.xvg files of the A state. Accepted formats: zip.
      --input_b_xvg_zip_path INPUT_B_XVG_ZIP_PATH
                            Path the zip file containing the dgdl.xvg files of the B state. Accepted formats: zip.
      --output_result_path OUTPUT_RESULT_PATH
                            Path to the TXT results file. Accepted formats: txt.
      --output_work_plot_path OUTPUT_WORK_PLOT_PATH
                            Path to the PNG plot results file. Accepted formats: png.
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

## Pmxmerge_ff
Wrapper class for the PMX merge_ff module.
### Get help
Command:
```python
pmxmerge_ff -h
```
    usage: pmxmerge_ff [-h] [-c CONFIG] --input_topology_path INPUT_TOPOLOGY_PATH --output_topology_path OUTPUT_TOPOLOGY_PATH
    
    Run PMX merge_ff module
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      --input_topology_path INPUT_TOPOLOGY_PATH
                            Path to the input ligand topologies as a zip file containing a list of itp files.
      --output_topology_path OUTPUT_TOPOLOGY_PATH
                            Path to the merged ligand topology file
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_topology_path** (*string*): Path to the input ligand topologies as a zip file containing a list of itp files. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand_itps.zip). Accepted formats: ZIP
* **output_topology_path** (*string*): Path to the merged ligand topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp). Accepted formats: ITP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (None) Container Image identifier..
* **container_volume_path** (*string*): (/inout) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmerge_ff.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
pmxmerge_ff --config config_pmxmerge_ff.yml --input_topology_path ligand_itps.zip --output_topology_path ligand.itp
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxmerge_ff.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
pmxmerge_ff --config config_pmxmerge_ff.json --input_topology_path ligand_itps.zip --output_topology_path ligand.itp
```

## Pmxcreate_top
Wrapper class for the PMX create_top module.
### Get help
Command:
```python
pmxcreate_top -h
```
    usage: pmxcreate_top [-h] [-c CONFIG] --input_topology1_path INPUT_TOPOLOGY1_PATH --input_topology2_path INPUT_TOPOLOGY2_PATH --output_topology_path OUTPUT_TOPOLOGY_PATH
    
    Run PMX create_top module
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      --input_topology1_path INPUT_TOPOLOGY1_PATH
                            Path to the input topology file 1
      --input_topology2_path INPUT_TOPOLOGY2_PATH
                            Path to the input topology file 2
      --output_topology_path OUTPUT_TOPOLOGY_PATH
                            Path to the complete ligand topology file
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_topology1_path** (*string*): Path to the input topology file 1. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp). Accepted formats: ITP
* **input_topology2_path** (*string*): Path to the input topology file 2. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp). Accepted formats: ITP
* **output_topology_path** (*string*): Path to the complete ligand topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand_top.zip). Accepted formats: ZIP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **force_field** (*string*): (amber99sb-star-ildn-mut.ff) Force-field to be included in the generated topology..
* **water** (*string*): (tip3p) Water model to be included in the generated topology..
* **system_name** (*string*): (Pmx topology) System name to be included in the generated topology..
* **mols** (*array*): ([[Protein,1],[Ligand,1]]) Molecules to be included in the generated topology..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (None) Container Image identifier..
* **container_volume_path** (*string*): (/inout) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxcreate_top.yml)
```python
properties:
  force_field: amber99sb-star-ildn-mut.ff
  mols:
  - - MOL
    - 1
  system_name: Pmx topology BioBB Tutorial
  water: spce

```
#### Command line
```python
pmxcreate_top --config config_pmxcreate_top.yml --input_topology1_path ligand.itp --input_topology2_path ligand.itp --output_topology_path ligand_top.zip
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxcreate_top.json)
```python
{
  "properties": {
    "force_field": "amber99sb-star-ildn-mut.ff",
    "water": "spce",
    "system_name": "Pmx topology BioBB Tutorial",
    "mols": [
      [
        "MOL",
        1
      ]
    ]
  }
}
```
#### Command line
```python
pmxcreate_top --config config_pmxcreate_top.json --input_topology1_path ligand.itp --input_topology2_path ligand.itp --output_topology_path ligand_top.zip
```

## Pmxgentop
Wrapper class for the PMX gentop module.
### Get help
Command:
```python
pmxgentop -h
```
    usage: pmxgentop [-h] [-c CONFIG] --input_top_zip_path INPUT_TOP_ZIP_PATH --output_top_zip_path OUTPUT_TOP_ZIP_PATH
    
    Wrapper class for the PMX gentop module
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      --input_top_zip_path INPUT_TOP_ZIP_PATH
                            Path to the input topology zip file
      --output_top_zip_path OUTPUT_TOP_ZIP_PATH
                            Path to the output topology zip file
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

## Pmxatom_mapping
Wrapper class for the PMX atom_mapping module.
### Get help
Command:
```python
pmxatom_mapping -h
```
    usage: pmxatom_mapping [-h] [-c CONFIG] --input_structure1_path INPUT_STRUCTURE1_PATH --input_structure2_path INPUT_STRUCTURE2_PATH --output_pairs1_path OUTPUT_PAIRS1_PATH --output_pairs2_path OUTPUT_PAIRS2_PATH --output_log_path OUTPUT_LOG_PATH [--output_structure1_path OUTPUT_STRUCTURE1_PATH] [--output_structure2_path OUTPUT_STRUCTURE2_PATH] [--output_morph1_path OUTPUT_MORPH1_PATH] [--output_morph2_path OUTPUT_MORPH2_PATH] [--output_scaffold1_path OUTPUT_SCAFFOLD1_PATH] [--output_scaffold2_path OUTPUT_SCAFFOLD2_PATH] [--output_score_path OUTPUT_SCORE_PATH]
    
    Run PMX atom mapping module
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
      --output_structure1_path OUTPUT_STRUCTURE1_PATH
                            Path to the superimposed structure for the ligand structure 1
      --output_structure2_path OUTPUT_STRUCTURE2_PATH
                            Path to the superimposed structure for the ligand structure 2
      --output_morph1_path OUTPUT_MORPH1_PATH
                            Path to the morphable atoms for the ligand structure 1
      --output_morph2_path OUTPUT_MORPH2_PATH
                            Path to the morphable atoms for the ligand structure 2
      --output_scaffold1_path OUTPUT_SCAFFOLD1_PATH
                            Path to the index of atoms to consider for the ligand structure 1
      --output_scaffold2_path OUTPUT_SCAFFOLD2_PATH
                            Path to the index of atoms to consider for the ligand structure 2
      --output_score_path OUTPUT_SCORE_PATH
                            Path to the morphing score. File type: output
    
    required arguments:
      --input_structure1_path INPUT_STRUCTURE1_PATH
                            Path to the input ligand structure file 1
      --input_structure2_path INPUT_STRUCTURE2_PATH
                            Path to the input ligand structure file 2
      --output_pairs1_path OUTPUT_PAIRS1_PATH
                            Path to the output pairs for the ligand structure 1
      --output_pairs2_path OUTPUT_PAIRS2_PATH
                            Path to the output pairs for the ligand structure 2
      --output_log_path OUTPUT_LOG_PATH
                            Path to the log file
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure1_path** (*string*): Path to the input ligand structure file 1. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb). Accepted formats: PDB
* **input_structure2_path** (*string*): Path to the input ligand structure file 2. File type: input. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb). Accepted formats: PDB
* **output_pairs1_path** (*string*): Path to the output pairs for the ligand structure 1. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_mapping_pairs.dat). Accepted formats: DAT, TXT
* **output_pairs2_path** (*string*): Path to the output pairs for the ligand structure 2. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_mapping_pairs.dat). Accepted formats: DAT, TXT
* **output_log_path** (*string*): Path to the log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atom_mapping.log). Accepted formats: LOG, TXT, OUT
* **output_structure1_path** (*string*): Path to the superimposed structure for the ligand structure 1. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb). Accepted formats: PDB
* **output_structure2_path** (*string*): Path to the superimposed structure for the ligand structure 2. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb). Accepted formats: PDB
* **output_morph1_path** (*string*): Path to the morphable atoms for the ligand structure 1. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb). Accepted formats: PDB
* **output_morph2_path** (*string*): Path to the morphable atoms for the ligand structure 2. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb). Accepted formats: PDB
* **output_scaffold1_path** (*string*): Path to the index of atoms to consider for the ligand structure 1. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx). Accepted formats: NDX
* **output_scaffold2_path** (*string*): Path to the index of atoms to consider for the ligand structure 2. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx). Accepted formats: NDX
* **output_score_path** (*string*): Path to the morphing score. File type: output. [Sample file](https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/morph_score.dat). Accepted formats: DAT, TXT
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **noalignment** (*boolean*): (False) Should the alignment method be disabled..
* **nomcs** (*boolean*): (False) Should the MCS method be disabled..
* **noH2H** (*boolean*): (True) Should non-polar hydrogens be discarded from morphing into any other hydrogen..
* **H2Hpolar** (*boolean*): (False) Should polar hydrogens be morphed into polar hydrogens..
* **H2Heavy** (*boolean*): (False) Should hydrogen be morphed into a heavy atom..
* **RingsOnly** (*boolean*): (False) Should rings only be used in the MCS search and alignemnt..
* **dMCS** (*boolean*): (False) Should the distance criterium be also applied in the MCS based search..
* **swap** (*boolean*): (False) Try swapping the molecule order which would be a cross-check and require double execution time..
* **nochirality** (*boolean*): (True) Perform chirality check for MCS mapping..
* **distance** (*number*): (0.05) Distance (nm) between atoms to consider them morphable for alignment approach..
* **timeout** (*integer*): (10) Maximum time (s) for an MCS search..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (None) Container Image identifier..
* **container_volume_path** (*string*): (/inout) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxatom_mapping.yml)
```python
properties:
  distance: 0.05
  noalignment: false

```
#### Command line
```python
pmxatom_mapping --config config_pmxatom_mapping.yml --input_structure1_path ligand.pdb --input_structure2_path ligand.pdb --output_pairs1_path ref_mapping_pairs.dat --output_pairs2_path ref_mapping_pairs.dat --output_log_path atom_mapping.log --output_structure1_path superimposed_ligand.pdb --output_structure2_path superimposed_ligand.pdb --output_morph1_path superimposed_ligand.pdb --output_morph2_path superimposed_ligand.pdb --output_scaffold1_path atoms_to_consider.ndx --output_scaffold2_path atoms_to_consider.ndx --output_score_path morph_score.dat
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/config/config_pmxatom_mapping.json)
```python
{
  "properties": {
    "noalignment": false,
    "distance": 0.05
  }
}
```
#### Command line
```python
pmxatom_mapping --config config_pmxatom_mapping.json --input_structure1_path ligand.pdb --input_structure2_path ligand.pdb --output_pairs1_path ref_mapping_pairs.dat --output_pairs2_path ref_mapping_pairs.dat --output_log_path atom_mapping.log --output_structure1_path superimposed_ligand.pdb --output_structure2_path superimposed_ligand.pdb --output_morph1_path superimposed_ligand.pdb --output_morph2_path superimposed_ligand.pdb --output_scaffold1_path atoms_to_consider.ndx --output_scaffold2_path atoms_to_consider.ndx --output_score_path morph_score.dat
```

## Pmxmutate
Wrapper class for the PMX mutate module.
### Get help
Command:
```python
pmxmutate -h
```
    usage: pmxmutate [-h] [-c CONFIG] --input_structure_path INPUT_STRUCTURE_PATH --output_structure_path OUTPUT_STRUCTURE_PATH [--input_b_structure_path INPUT_B_STRUCTURE_PATH]
    
    Run PMX mutate module
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
      --input_b_structure_path INPUT_B_STRUCTURE_PATH
                            Path to the mutated input structure file
    
    required arguments:
      --input_structure_path INPUT_STRUCTURE_PATH
                            Path to the input structure file
      --output_structure_path OUTPUT_STRUCTURE_PATH
                            Path to the output structure file
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
* **container_image** (*string*): (None) Container Image identifier..
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
    "container_path": "docker"
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
