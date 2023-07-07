# !/usr/bin/env python3

"""Module containing the PMX ligand_hybrid class and the command line interface."""
import os
import sys
from pathlib import Path
import shutil
import argparse
from typing import Mapping
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger


class Pmxligand_hybrid(BiobbObject):
    """
    | biobb_pmx Pmxligand_hybrid
    | Wrapper class for the `PMX ligand_hybrid <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_structure1_path (str): Path to the input ligand structure file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_structure2_path (str): Path to the input ligand structure file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_topology1_path (str): Path to the input ligand topology file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp>`_. Accepted formats: itp (edam:format_3883).
        input_topology2_path (str): Path to the input ligand topology file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp>`_. Accepted formats: itp (edam:format_3883).
        input_pairs_path (str) (Optional): Path to the input atom pair mapping. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_mapping_pairs.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        input_scaffold1_path (str) (Optional): Path to the index of atoms to consider for the ligand structure 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx>`_. Accepted formats: ndx (edam:format_2033).
        input_scaffold2_path (str) (Optional): Path to the index of atoms to consider for the ligand structure 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx>`_. Accepted formats: ndx (edam:format_2033).
        output_log_path (str): Path to the log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atom_mapping.log>`_. Accepted formats: log (edam:format_2330), txt (edam:format_2330), out (edam:format_2330).
        output_structure1_path (str): Path to the output hybrid structure based on the ligand 1. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_structure2_path (str): Path to the output hybrid structure based on the ligand 2. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_topology_path (str): Path to the output hybrid topology. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ligand_hybrid.itp>`_. Accepted formats: itp (edam:format_3883).
        output_atomtypes_path (str): Path to the atom types for the output hybrid topology. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ligand_hybrid_atomtypes.itp>`_. Accepted formats: itp (edam:format_3883).

        properties (dic):
            * **fit** (*bool*) - (False) Fit ligand structure 1 onto ligand structure 2 (Only used if input_pairs_path is provided).
            * **split** (*bool*) - (False) Split the topology into separate transitions.
            * **scDUMm** (*float*) - (1.0) Scale dummy masses using the counterpart atoms.
            * **scDUMa** (*float*) - (1.0) Scale bonded dummy angle parameters.
            * **scDUMd** (*float*) - (1.0) Scale bonded dummy dihedral parameters.
            * **deAng** (*bool*) - (False) Decouple angles composed of 1 dummy and 2 non-dummies.
            * **distance** (*float*) - (0.05) Distance (nm) between atoms to consider them morphable for alignment approach (Only used if input_pairs_path is not provided).
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - (None) Container Image identifier.
            * **container_volume_path** (*str*) - ("/inout") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_pmx.pmxbiobb.pmxligand_hybrid import pmxligand_hybrid
            prop = {
                'fit' : True,
                'distance': 0.05
            }
            pmxligand_hybrid(input_structure1_path='/path/to/myStructure1.pdb',
                    input_structure2_path='/path/to/myStructure2.pdb',
                    input_topology1_path='/path/to/myTopology1.pdb',
                    input_topology2_path='/path/to/myTopology2.pdb',
                    input_pairs_path='/path/to/myPairs.dat',
                    output_log_path='/path/to/myLog.log',
                    output_structure1_path='/path/to/myStructureOutput1.pdb',
                    output_structure2_path='/path/to/myStructureOutput2.pdb',
                    output_topology_path='/path/to/myTopologyOutput.pdb',
                    output_atomtypes_path='/path/to/myAtomTypesOutput.pdb',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX ligand_hybrid
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_structure1_path: str, input_structure2_path: str, input_topology1_path: str, input_topology2_path: str,
                 output_log_path: str, output_structure1_path: str, output_structure2_path: str, output_topology_path: str, output_atomtypes_path: str,
                 input_scaffold1_path: str = None, input_scaffold2_path: str = None, input_pairs_path: str = None,
                 properties: Mapping = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure1_path": input_structure1_path, "input_structure2_path": input_structure2_path,
                   "input_topology1_path": input_topology1_path, "input_topology2_path": input_topology2_path,
                   "input_scaffold1_path": input_scaffold1_path, "input_scaffold2_path": input_scaffold2_path,
                   "input_pairs_path": input_pairs_path},
            "out": {"output_structure1_path": output_structure1_path, "output_structure2_path": output_structure2_path,
                    "output_topology_path": output_topology_path, "output_atomtypes_path": output_atomtypes_path,
                    "output_log_path": output_log_path}
        }

        # Properties specific for BB
        # self.fit = properties.get('fit', False)
        # self.split = properties.get('split', False)
        # self.scDUMm = properties.get('scDUMm', 1.0)
        # self.scDUMa = properties.get('scDUMa', 1.0)
        # self.scDUMd = properties.get('scDUMd', 1.0)
        # self.deAng = properties.get('deAng', False)
        # self.distance = properties.get('distance', 0.05)

        self.fit = properties.get('fit')
        self.split = properties.get('split')
        self.scDUMm = properties.get('scDUMm')
        self.scDUMa = properties.get('scDUMa')
        self.scDUMd = properties.get('scDUMd')
        self.deAng = properties.get('deAng')
        self.distance = properties.get('distance')

        # Properties common in all PMX BB
        self.gmx_lib = properties.get('gmx_lib', None)
        if not self.gmx_lib and os.environ.get('CONDA_PREFIX'):
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
            self.gmx_lib = str(
                Path(os.environ.get('CONDA_PREFIX')).joinpath(f"lib/python{python_version}/site-packages/pmx/data/mutff/"))
            if properties.get('container_path'):
                self.gmx_lib = str(Path('/usr/local/').joinpath("lib/python3.7/site-packages/pmx/data/mutff/"))
        self.binary_path = properties.get('binary_path', 'pmx')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Pmxmutate <pmx.pmxmutate.Pmxmutate>` pmx.pmxmutate.Pmxmutate object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Check if executable exists
        if not self.container_path:
            if not Path(self.binary_path).is_file():
                if not shutil.which(self.binary_path):
                    raise FileNotFoundError(
                        'Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.binary_path)

        self.cmd = [self.binary_path, 'ligandHybrid',
                    '-i1', self.stage_io_dict["in"]["input_structure1_path"],
                    '-i2', self.stage_io_dict["in"]["input_structure2_path"],
                    '-itp1', self.stage_io_dict["in"]["input_topology1_path"],
                    '-itp2', self.stage_io_dict["in"]["input_topology2_path"],
                    '-pairs', self.stage_io_dict["in"]["input_pairs_path"],
                    '-oA', self.stage_io_dict["out"]["output_structure1_path"],
                    '-oB', self.stage_io_dict["out"]["output_structure2_path"],
                    '-oitp', self.stage_io_dict["out"]["output_topology_path"],
                    '-offitp', self.stage_io_dict["out"]["output_atomtypes_path"],
                    '-log', self.stage_io_dict["out"]["output_log_path"]
                    ]

        if self.stage_io_dict["in"].get("output_scaffold1_path"):
            self.cmd.append('-n1')
            self.cmd.append(self.stage_io_dict["in"]["output_scaffold1_path"])

        if self.stage_io_dict["in"].get("output_scaffold2_path"):
            self.cmd.append('-n2')
            self.cmd.append(self.stage_io_dict["in"]["output_scaffold2_path"])

        if self.fit:
            self.cmd.append('--fit')
        if self.split:
            self.cmd.append('--split')
        if self.deAng:
            self.cmd.append('--deAng')
        if self.distance:
            self.cmd.append('--d')
            self.cmd.append(str(self.distance))
        if self.scDUMm:
            self.cmd.append('--scDUMm')
            self.cmd.append(str(self.scDUMm))
        if self.scDUMa:
            self.cmd.append('--scDUMa')
            self.cmd.append(str(self.scDUMa))
        if self.scDUMd:
            self.cmd.append('--scDUMd')
            self.cmd.append(str(self.scDUMd))

        if self.gmx_lib:
            self.env_vars_dict['GMXLIB'] = self.gmx_lib

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        self.tmp_files.append(self.stage_io_dict.get("unique_dir"))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def pmxligand_hybrid(input_structure1_path: str, input_structure2_path: str, input_topology1_path: str, input_topology2_path: str,
                     output_log_path: str, output_structure1_path: str, output_structure2_path: str, output_topology_path: str, output_atomtypes_path: str,
                     input_scaffold1_path: str = None, input_scaffold2_path: str = None, input_pairs_path: str = None,
                     properties: dict = None, **kwargs) -> int:
    """Execute the :class:`Pmxligand_hybrid <pmx.pmxmutate.Pmxligand_hybrid>` class and
    execute the :meth:`launch() <pmx.pmxligand_hybrid.Pmxligand_hybrid.launch> method."""

    return Pmxligand_hybrid(input_structure1_path=input_structure1_path, input_structure2_path=input_structure2_path,
                            input_topology1_path=input_topology1_path, input_topology2_path=input_topology2_path,
                            output_log_path=output_log_path,
                            output_structure1_path=output_structure1_path, output_structure2_path=output_structure2_path,
                            output_topology_path=output_topology_path, output_atomtypes_path=output_atomtypes_path,
                            input_scaffold1_path=input_scaffold1_path, input_scaffold2_path=input_scaffold2_path,
                            input_pairs_path=input_pairs_path,
                            properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Run PMX ligand hybrid module",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure1_path', required=True, help="Path to the input ligand structure file 1")
    required_args.add_argument('--input_structure2_path', required=True, help="Path to the input ligand structure file 2")
    required_args.add_argument('--input_topology1_path', required=True, help="Path to the input ligand topology file 1")
    required_args.add_argument('--input_topology2_path', required=True, help="Path to the input ligand topology file 2")
    required_args.add_argument('--output_structure1_path', required=True, help="Path to the output ligand structure file 1")
    required_args.add_argument('--output_structure2_path', required=True, help="Path to the output ligand structure file 2")
    required_args.add_argument('--output_topology1_path', required=True, help="Path to the output ligand topology file 1")
    required_args.add_argument('--output_topology2_path', required=True, help="Path to the output ligand topology file 2")
    required_args.add_argument('--output_log_path', required=True, help="Path to the log file")
    parser.add_argument('--input_scaffold1_path', required=False, help="Path to the index of atoms to consider for the ligand structure 1")
    parser.add_argument('--input_scaffold2_path', required=False, help="Path to the index of atoms to consider for the ligand structure 2")
    parser.add_argument('--input_pairs_path', required=False, help="Path to the input atom pair mapping.")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    pmxligand_hybrid(input_structure1_path=args.input_structure1_path, input_structure2_path=args.input_structure2_path,
                     input_topology1_path=args.input_topology1_path, input_topology2_path=args.input_topology2_path,
                     input_scaffold1_path=args.input_scaffold1_path, input_scaffold2_path=args.input_scaffold2_path,
                     input_pairs_path=args.input_pairs_path, output_log_path=args.output_log_path,
                     output_structure1_path=args.output_structure1_path, output_structure2_path=args.output_structure2_path,
                     output_topology1_path=args.output_topology1_path, output_topology2_path=args.output_topology2_path,
                     properties=properties)


if __name__ == '__main__':
    main()
